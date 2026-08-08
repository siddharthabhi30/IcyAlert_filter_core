# 2D Linear System - Liang-Kleeman Information Transfer

Calculates Liang-Kleeman (LK) information transfer ($T_{2\rightarrow1}$) on a 2D stochastic linear system.

## Configuration
Modify `config.py` to change parameters (e.g., integration step, noise variance, simulation steps).

## Running Experiments

### 1. Ensemble Kalman Filter (EnKF) Simulation
Assimilates noisy observations using a Stochastic EnKF. Calculates $T_{2\rightarrow1}$ from the ensemble covariance at each step.
```bash
python run_simulation.py
python plot_results.py
```

### 2. Time-Series Estimator
Runs a single stochastic trajectory and calculates covariance over the time dimension (Equation 1, Vannitsem et al., 2019).
```bash
python time_series_estimator.py
```
