import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    results_file = 'results.csv'
    
    if not os.path.exists(results_file):
        print(f"Error: {results_file} not found. Please run run_simulation.py first.")
        return
        
    print(f"Loading {results_file}...")
    df = pd.parse_csv(results_file) if hasattr(pd, 'parse_csv') else pd.read_csv(results_file)
    
    # Calculate a rolling average to smooth out the noise
    window_size = 100
    df['t21_forecast_smooth'] = df['t21_forecast'].rolling(window=window_size).mean()
    df['t21_analysis_smooth'] = df['t21_analysis'].rolling(window=window_size).mean()

    # The theoretical physical steady state for T_{2->1} from the paper
    # (a12 * P12 / P11) -> 0.5 * (0.00125 / 0.005625) = 0.111111...
    theoretical_steady_state = 0.111111
    
    plt.figure(figsize=(12, 6))
    
    # Plot smoothed curves
    plt.plot(df['step'], df['t21_forecast_smooth'], label='EnKF Forecast (Smoothed)', color='blue')
    plt.plot(df['step'], df['t21_analysis_smooth'], label='EnKF Analysis (Smoothed)', color='green')
    
    # Plot theoretical line
    plt.axhline(y=theoretical_steady_state, color='red', linestyle='--', label='Theoretical Physical Steady State')
    
    plt.title('Liang-Kleeman Information Transfer ($T_{2\\rightarrow 1}$) over time')
    plt.xlabel('Simulation Steps')
    plt.ylabel('$T_{2\\rightarrow 1}$')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_image = 't21_plot.png'
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Plot saved successfully to {output_image}")

if __name__ == "__main__":
    main()
