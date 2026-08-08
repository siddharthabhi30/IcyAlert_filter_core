# TvLK — My Interpretation

## Goal

The goal is to understand the causality between soil moisture and air temperature: how much each one affects the other.

$$
T_{2\rightarrow1}
$$

measures the influence of $X_2$ on $X_1$. Similarly, $T_{1\rightarrow2}$ measures the influence of $X_1$ on $X_2$.

---

## Original LK

[Liang (2014), “Unraveling the Cause-Effect Relation between Time Series”](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.90.052150)

Original LK uses the available time series. It first constructs:

$$
\dot X_j(t) = \frac{X_j(t+k\Delta t)-X_j(t)}{k\Delta t}
$$

It then calculates:

$$
C_{ij} := \overline{ \left(X_i-\overline{X_i}\right) \left(X_j-\overline{X_j}\right) }
$$

$$
C_{i,dj} := \overline{ \left(X_i-\overline{X_i}\right) \left(\dot X_j-\overline{\dot X_j}\right) }
$$

- $C_{12}$ comes from the paired series $X_1,X_2$.
- $C_{2,d1}$ comes from the paired series $X_2,\dot X_1$.
- These covariances need multiple time samples. They cannot be calculated from one observation.

### Small example

Assume $X_1$ and $X_2$ are the two variables whose causality is being studied.

$$
X_1=[10,11,13,16],\qquad X_2=[20,21,23,24].
$$

For $\Delta t=1$:

$$
\dot X_1=[1,2,3].
$$

Therefore, $C_{2,d1}$ is calculated from:

$$
(20,1),\quad(21,2),\quad(23,3).
$$

Liang (2014), Eq. (10):

$$
T_{2\rightarrow1} = \frac{ C_{11}C_{12}C_{2,d1} - C_{12}^{2}C_{1,d1} }{ C_{11}^{2}C_{22} - C_{11}C_{12}^{2} }
$$

The result is one $T_{2\rightarrow1}$ value for the selected time-series record.

---

## Time-Varying LK

[Hagan et al. (2019), “A Time-Varying Causality Formalism Based on the Liang–Kleeman Information Flow for Analyzing Directed Interactions in Nonstationary Climate Systems”](https://journals.ametsoc.org/view/journals/clim/32/21/jcli-d-18-0881.1.xml)

Soil-moisture and air-temperature interaction changes with time and across seasons. The 2019 paper replaces the fixed covariances with $P(t)$ from a square-root Kalman filter.

The original LK formula uses $C$. The time-varying formula replaces the same entries with $P(t)$:

$$
C_{11}\rightarrow P_{11}(t),\qquad
C_{12}\rightarrow P_{12}(t),\qquad
C_{22}\rightarrow P_{22}(t),
$$

$$
C_{1,d1}\rightarrow P_{1,d1}(t),\qquad
C_{2,d1}\rightarrow P_{2,d1}(t).
$$

Hagan et al. (2019), Eq. (15):

$$
T_{2\rightarrow1,t} = \frac{P_{12}}{P_{11}} \frac{ -P_{12}P_{1,d1}+P_{11}P_{2,d1} }{ P_{11}P_{22}-P_{12}^{2} }
$$

The filter updates $P(t)$, which is used to calculate causality at each time step.

### Process model

$$
x_k=A x_{k-1}+B u_k+w_{k-1},
$$

$$
y_k=H x_k+v_k.
$$

For the second TvLK version, the paper says:

> “the transition matrix functions in Eq. (9) are first determined by fitting an autoregressive model to the data and performing a Kalman filter on it.”

For this version, the process model is known before the covariance is estimated.

### $Q$ and $R$

$$
E[w_kw_k^T]=Q,
\qquad
E[v_kv_k^T]=R.
$$

The paper calculates $Q(t)$ and $R(t)$ offline using EWMA or UWMA, then supplies them to the Kalman filter at each time step.

> “obtaining an accurate result is highly dependent on the offline computation of Q and R.”

---

## [Sid] Notes

- The paper does not show how $P_{1,d2}$ and $P_{2,d1}$ are produced. I am assuming that $\dot X_1$ and $\dot X_2$ are included as state variables, so these covariance entries appear in $P$. This is not confirmed by the paper.

- Tommy wanted to see whether $Q(t)$ and $R(t)$ could be calculated dynamically.

- KalmanNet learns the Kalman gain but does not explicitly output covariance matrices. A possible modification is to make the DNN output a lower-triangular Cholesky factor $L$ with a positive diagonal and construct the covariance as $LL^T$, making it positive definite.

---

## Further Reading

- [Zhou et al. (2024), multivariate time-varying LK](https://doi.org/10.1175/JCLI-D-23-0207.1)
- [Lien et al. (2025), LIM–LK](https://doi.org/10.1103/5cd4-5cb4)
- [Observational causality by states and interaction type (2025)](https://www.nature.com/articles/s42005-025-02447-w)
- [Richard Kleeman — Information Theory, Predictability and Disequilibrium](https://www.math.nyu.edu/faculty/kleeman/syllabusinfo.html)
- [Richard Kleeman — Lecture 11 PDF](https://math.nyu.edu/~kleeman/infolect11.pdf)