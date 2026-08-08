import torch
import matplotlib.pyplot as plt
import config
from process_model import process_model
from enKF import get_covariance
from lk_metrics import calc_T2_to_1

def calc_t21_from_trajectory(X: torch.Tensor) -> float:
    """
    Calculates T_{2->1} using the simplistic formula by re-using 
    the core covariance and metrics functions.
    """
    if X.shape[0] < 2:
        return 0.0
        
    # 1. Get covariance matrix across the time dimension (L steps)
    cov_matrix = get_covariance(X)
    
    # 2. Calculate T_2->1 using the imported metric function
    # (which evaluates a12 * P12 / P11)
    return calc_T2_to_1(cov_matrix)

def plot_t21_convergence(steps: list, t21_values: list):
    """
    Plots the convergence of T_{2->1} over trajectory length.
    """
    plt.figure(figsize=(10, 6))
    
    # Plot estimator
    plt.plot(steps, t21_values, label='Simplistic Formula ($a_{12} C_{12} / C_{11}$)', color='orange', linewidth=2)
    
    # Theoretical physical stationary state
    plt.axhline(y=config.THEORETICAL_STEADY_STATE, color='red', linestyle='--', label='Theoretical Physical Steady State')
    
    plt.title('Convergence of Time-Series Information Transfer Estimator')
    plt.xlabel('Trajectory Length (L steps)')
    plt.ylabel('Estimated T$_{2\\rightarrow 1}$')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_image = 'timeseries_t21_convergence.png'
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Plot saved successfully to {output_image}")

def run_time_series_experiment():
    """
    Runs a single stochastic trajectory, records it, and evaluates T21.
    """
    print(f"Initializing 1 trajectory on {config.DEVICE}...")
    x = torch.randn(1, 2, dtype=config.DTYPE, device=config.DEVICE)
    
    # Burn-in
    print(f"Running burn-in for {config.BURN_IN_STEPS} steps...")
    for _ in range(config.BURN_IN_STEPS):
        x = process_model(x)
        
    print(f"Running main trajectory for {config.TS_TOTAL_STEPS} steps (evaluating T21 every {config.TS_PLOT_STEP} steps)...")
    trajectory = []
    
    # Arrays to save the (step, T21) data for plotting
    steps_recorded = []
    t21_values = []
    
    for step in range(1, config.TS_TOTAL_STEPS + 1):
        x = process_model(x)
        trajectory.append(x.squeeze(0))
        
        if step % config.TS_PLOT_STEP == 0:
            X_tensor = torch.stack(trajectory, dim=0)
            
            t21 = calc_t21_from_trajectory(X_tensor)
            
            steps_recorded.append(step)
            t21_values.append(t21)
            
            print(f"Step {step}/{config.TS_TOTAL_STEPS} | T2->1 = {t21:.6f}")
            
    plot_t21_convergence(steps_recorded, t21_values)

if __name__ == "__main__":
    run_time_series_experiment()
