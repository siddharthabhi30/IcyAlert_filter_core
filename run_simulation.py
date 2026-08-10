import torch
import csv
import os
import config
from process_model import process_model
from observation_model import observation_model
from enKF import enkf_update, get_covariance
from lk_metrics import calc_T2_to_1

def main():
    print("Starting EnKF + Liang-Kleeman Simulation...")
    
    # --------------------------------------------------------------------------
    # Initialization
    # --------------------------------------------------------------------------
    # 1. Initialize the "True" state (just 1 particle)
    x_true = torch.randn(1, 2, dtype=config.DTYPE, device=config.DEVICE)
    
    # 2. Initialize the Ensemble (NUM_PARTICLES)
    x_ensemble = torch.randn(config.NUM_PARTICLES, 2, dtype=config.DTYPE, device=config.DEVICE)
    
    # --------------------------------------------------------------------------
    # Burn-In Phase (Run process model without observing)
    # --------------------------------------------------------------------------
    burn_in_ensemble = torch.randn(
        config.NUM_PARTICLES,
        2,
        dtype=config.DTYPE,
        device=config.DEVICE,
    )
    results = []

    print(f"Running process-only burn-in for {config.BURN_IN_STEPS} steps...")
    for step in range(config.BURN_IN_STEPS):
        burn_in_ensemble = process_model(burn_in_ensemble)
        cov = get_covariance(burn_in_ensemble)
            
        t21 = calc_T2_to_1(cov)
        results.append({
            "step": step - config.BURN_IN_STEPS,
            "t21_forecast": t21,
            "t21_analysis": t21,
            "t21_momentum": t21,
        })
    
    # ----------------------------------------------------------------------
    # Assimilation phase
    # ----------------------------------------------------------------------
    x_ensemble = burn_in_ensemble.clone()
    x_true = burn_in_ensemble[0:1].clone()
    momentum_covariance = get_covariance(burn_in_ensemble)
    
    print(f"Running simulation for {config.SIM_STEPS} steps...")
    for step in range(config.SIM_STEPS):
        # 1. Advance the true state
        x_true = process_model(x_true)
        
        # 2. Get a noisy observation from the true state
        y_obs = observation_model(x_true).squeeze(0)  # Shape: (2,)
        
        # 3. Forecast step: Advance the ensemble
        x_forecast = process_model(x_ensemble)
        
        # Calculate T2->1 on Forecast Covariance (Optional, can record both)
        cov_forecast = get_covariance(x_forecast)
        t21_forecast = calc_T2_to_1(cov_forecast)
        
        momentum_covariance = config.ALPHA * momentum_covariance + (1.0 - config.ALPHA) * cov_forecast
        t21_momentum = calc_T2_to_1(momentum_covariance)
        
        # 4. Analysis step: Update the ensemble with the observation
        x_analysis = enkf_update(x_forecast, y_obs)
        
        # Calculate T2->1 on Analysis Covariance
        cov_analysis = get_covariance(x_analysis)
        t21_analysis = calc_T2_to_1(cov_analysis)
        
        # Store results for this step
        results.append({
            'step': step,
            't21_forecast': t21_forecast,
            't21_analysis': t21_analysis,
            't21_momentum': t21_momentum
        })
        
        # Update ensemble for the next time step
        x_ensemble = x_analysis
        
        if (step + 1) % 1000 == 0:
            print(f"Step {step + 1}/{config.SIM_STEPS} complete.")
            
    # --------------------------------------------------------------------------
    # Save Results
    # --------------------------------------------------------------------------
    output_file = 'results.csv'
    print(f"Saving results to {output_file}...")
    
    keys = results[0].keys()
    with open(output_file, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
        
    print("Simulation finished successfully!")
    
    # Automatically plot the results
    import plot_results
    print("Generating plot automatically...")
    plot_results.main()

if __name__ == "__main__":
    main()
