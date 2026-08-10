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
    if 't21_momentum' in df.columns:
        df['t21_momentum_smooth'] = df['t21_momentum'].rolling(window=window_size).mean()

    paper_reference_t21 = 0.111111
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(
        df['step'],
        df['t21_forecast_smooth'],
        label='EnKF Forecast (100-step rolling mean)',
        color='blue',
    )
    plt.plot(
        df['step'],
        df['t21_analysis_smooth'],
        label='EnKF Analysis (100-step rolling mean)',
        color='green',
    )
    if 't21_momentum_smooth' in df.columns:
        plt.plot(
            df['step'],
            df['t21_momentum_smooth'],
            label='Momentum Covariance (100-step rolling mean)',
            color='purple',
        )
    
    # Plot theoretical line
    plt.axhline(
        y=paper_reference_t21,
        color='red',
        linestyle='--',
        label='Paper reference $T_{2\\rightarrow 1}=0.1111$',
    )
    
    # Plot vertical line for DA start
    plt.axvline(
        x=0,
        color='black',
        linestyle='--',
        label='EnKF DA Starts',
    )
    
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
