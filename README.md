# IcyAlert: EnKF and Information-Transfer Experiment

This repository tests how the Liang-Kleeman information-transfer metric ($T_{2\rightarrow1}$) behaves before and during Ensemble Kalman Filter (EnKF) assimilation.

There are two experiments:

1. reproduce the stationary $T_{2\rightarrow1}$ reference using a long process-model time series;
2. compare forecast, posterior, and momentum covariance estimates during EnKF assimilation.

Covariance momentum is an experimental diagnostic. It is not part of the EnKF update and is not yet a validated method for preserving physical causality.

## ⚙️ Process Model (Particle Propagation)

To propagate each particle, the experiment uses a **2D Stochastic Linear System** (from [Vannitsem et al., 2019](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019GL084329)). The model applies **Euler-Maruyama numerical integration** to advance the state according to the following equations:

$$ dx_1 = (a_{11}x_1 + a_{12}x_2) dt + \text{noise} $$
$$ dx_2 = (a_{21}x_1 + a_{22}x_2) dt + \text{noise} $$

For this controlled experiment, the system is defined by the following exact parameters:
* $a_{11} = -1.0$
* $a_{12} = 0.5$ (The direct connection from $x_2 \rightarrow x_1$)
* $a_{21} = 0.0$
* $a_{22} = -1.0$

Additive stochastic noise is applied independently at each time step.

## 🔬 Experiments and Results

### 1. Stationary time-series reference

`time_series_estimator.py` runs one stochastic process-model trajectory. After a 10,000-step burn-in, it collects 50,000 states and calculates covariance across time. The estimate converges towards the stationary reference $T_{2\rightarrow1}\approx0.1111$.

### 2. EnKF experiment

`run_simulation.py` first advances a 1,000-member process-model ensemble for 10,000 steps without observations. It then runs 20,000 assimilation steps, observing both variables with $H=I$.

At every assimilation step, it records $T_{2\rightarrow1}$ from:

- the forecast ensemble covariance;
- the posterior ensemble covariance;
- a momentum average of forecast covariances.

The posterior-covariance estimate drops away from the stationary reference after assimilation begins. This does not show that the underlying physical causality disappeared. It shows that $T_{2\rightarrow1}$ calculated from the posterior uncertainty covariance differs from the stationary process covariance in this experiment.

The momentum covariance is

$$
P^{\mathrm{mom}}_t
=
\alpha P^{\mathrm{mom}}_{t-1}
+
(1-\alpha)P^f_t,
\qquad \alpha=0.99999.
$$

It changes slowly because it retains almost all of its previous value. It is tracked only for comparison and is not used to update or resample the EnKF ensemble.

**Visualizations of these results:**
* **[Transient vs. Stationary Analysis Plot](./timeseries_t21_convergence.png)**: Displays how the time-dependent transient rate $T_{2\rightarrow 1}(t)$ behaves relative to the asymptotic stationary climatological baseline.
* **[Information Transfer ($T_{2\rightarrow 1}$) Plot](./t21_plot.png)**: Shows the continuous transient metric across the burn-in and assimilation phases.

## 📁 Codebase Overview

* **`config.py`**: Centralizes configuration parameters, including the 2D SDE parameters, noise variances ($Q$, $R$), step sizes, and the momentum $\alpha$ constant.
* **`process_model.py`**: Defines the forward integration of the 2D linear SDE state.
* **`observation_model.py`**: Defines the observation operator ($y = Hx + v$).
* **`enKF.py`**: Implements the stochastic Ensemble Kalman Filter update steps and covariance calculations.
* **`lk_metrics.py`**: Calculates the Liang-Kleeman Information Transfer causality metric $T_{2\rightarrow 1} = a_{12} (P_{12} / P_{11})$.
* **`run_simulation.py`**: Manages the 1000-member ensemble through the continuous burn-in and assimilation phases, and records all metrics to a CSV.
* **`plot_results.py`**: Reads the output CSV and generates `t21_plot.png`. It applies a 100-step rolling window to smooth the noisy plot lines and marks the start of the DA phase.
* **`time_series_estimator.py`**: Runs one long stochastic trajectory and calculates covariance across time to reproduce the stationary reference.

## 🚀 Usage

1. **Run the simulation**:
   ```bash
   python run_simulation.py
   ```
   This executes all 30,000 steps, outputs data to `results.csv`, and automatically generates the plots.

2. **Generate the main plot manually**:
   ```bash
   python plot_results.py
   ```

3. **Run the stationary time-series reference**:
   ```bash
   python time_series_estimator.py
   ```
