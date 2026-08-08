# 2D Linear System - Liang-Kleeman Information Transfer

This directory contains two distinct experiments for calculating the Liang-Kleeman (LK) information transfer ($T_{2\rightarrow1}$) on a 2D stochastic linear system (based on Vannitsem et al., 2019).

## Configuration
All parameters for the physical system, noise variance, and experiment run-times are centrally located in **`config.py`**. 
Modify this file to change the integration step (`DT`), coupling coefficients (`A11`, `A12`, etc.), or the number of simulation steps.

---

## Experiment 1: Ensemble Kalman Filter (EnKF) Simulation
This experiment runs a "true" physical state alongside an ensemble of particles. It assimilates noisy observations at every step using a Stochastic EnKF. The information transfer $T_{2\rightarrow1}$ is calculated cross-sectionally over the ensemble covariance matrix at each time step.

### How to run:
1. **Run the simulation**: 
   ```bash
   python run_simulation.py
   ```
   *This will run the burn-in, simulate the specified number of steps, and save the results (Forecast and Analysis $T_{2\rightarrow1}$) to `results.csv`.*

2. **Plot the results**:
   ```bash
   python plot_results.py
   ```
   *This reads `results.csv`, calculates a moving average to smooth the noisy ensemble estimates, and generates `t21_plot.png`.*

---

## Experiment 2: Time-Series Estimator
This experiment strictly follows the finite-time-series approach (Equation 1) described in the 2019 paper. Instead of an ensemble, it runs **one single stochastic trajectory** for a long period of time and calculates the covariance over the time dimension.

### How to run:
1. **Run and plot the trajectory**:
   ```bash
   python time_series_estimator.py
   ```
   *This will run the trajectory for the number of steps defined in `config.py` (`TS_TOTAL_STEPS`). It periodically evaluates the simplistic LK formula ($a_{12} C_{12} / C_{11}$) on the accumulated trajectory and saves the convergence plot directly to `timeseries_t21_convergence.png`.*

---

## Core Modules
- **`process_model.py`**: The raw stochastic Euler-Maruyama integration step $x_{t+1} = x_t + f(x_t)dt + \xi$.
- **`observation_model.py`**: Generates noisy observations $y = Hx + v$.
- **`enKF.py`**: Contains the stochastic EnKF update step and the ensemble covariance calculator.
- **`lk_metrics.py`**: The mathematical formula for $T_{2\rightarrow1}$. Used by both experiments to adhere to the DRY principle.
