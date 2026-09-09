# IcyAlert Covariance Experiment

## Premise

Liang--Kleeman information transfer depends on the covariance structure of the system. This experiment tests what happens when the covariance supplied to the LK equation is the posterior covariance from data assimilation.

Two equivalent filters are compared:

- an Ensemble Kalman Filter (EnKF), where covariance is estimated across ensemble members;
- an analytical Kalman filter, where the covariance matrix is propagated directly.

Both use the same process model. The observation variance $R$ is varied to control how strongly the filters trust observations.

## Process model

The process model is

```math
dX_1=(a_{11}X_1+a_{12}X_2)\,dt+\sqrt{q}\,dW_1,
```

```math
dX_2=(a_{21}X_1+a_{22}X_2)\,dt+\sqrt{q}\,dW_2.
```

with $a_{11}=a_{22}=-1$, $a_{12}=0.5$, $a_{21}=0$ (information flows only $2\rightarrow1$), process-noise variance $q=0.01$, and $dt=0.1$.

## Observation model

```math
y_t=HX_t+v_t,\qquad H=I,\qquad v_t\sim\mathcal{N}(0,R\,I).
```

$X_t$ is the truth trajectory (the process model run once), and $R$ is the observation variance.

## Information transfer

For this system, information transfer from $X_2$ to $X_1$ is

```math
T_{2\rightarrow1}(t)
=a_{12}\frac{P_{12}(t)}{P_{11}(t)},
\qquad a_{12}=0.5.
```

Here, $P_{12}(t)$ is the covariance between $X_1$ and $X_2$, and $P_{11}(t)$ is the variance of $X_1$, at time $t$.

The dashed curve in each figure is the process-only covariance reference, obtained without observation updates.

## Results

### Analytical Kalman filter

![Analytical Kalman dynamic information transfer](./kalman_t21_vs_R.png)

### Ensemble Kalman filter

![EnKF dynamic information transfer](./enkf_t21_vs_R.png)

Both methods behave the same: reducing $R$ contracts the posterior covariance and pushes $T_{2\rightarrow1}$ toward zero (the EnKF is noisier from finite-ensemble sampling). The posterior uncertainty covariance is a different object from the process covariance used by the reference LK calculation, and small observation noise compresses the structure that calculation needs.

## Forecast vs assimilated

Assimilation happens at every step. At each time $t$ we plot the forecast $T_{2\rightarrow1}$, then assimilate. The covariance never reaches the ideal value — assimilation destroys it at every time $t$. Both curves stay well below the process-only value ($\approx 0.11$, the free run with no assimilation).

![Forecast vs assimilated T21](./forecast_vs_assim_t21.png)

One noise level, $R=0.05$: both settle around $0.06$, about halfway between the ideal $\approx 0.11$ and zero.

## Run

```bash
python run_kalman_covariance.py
python run_enkf_covariance.py
python run_forecast_vs_assim.py
```

Computing $T_{2\rightarrow1}$ with the tendency $dX$ written out explicitly converges to the same $a_{12}P_{12}/P_{11}$ value — see [enkf_dx_t21_vs_R.png](./enkf_dx_t21_vs_R.png) (`python run_dx_explicit.py`).
