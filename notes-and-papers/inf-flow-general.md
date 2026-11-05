

## Mutual information

$$
I(X; Y) = H(X) - H(X \mid Y)
$$

Mutual information is the expected reduction in uncertainty in $X$ with perfect knowledge of $Y$. This is just the conditional thing.

Mutual information is symmetric.

## TLMI (time lagged mutual information)

Same formula, with the two variables at different times: $X$ at the later time $t$, $Y$ at the initial time $t_0$.

$$
I(X(t); Y(t_0)) = H(X(t)) - H(X(t) \mid Y(t_0))
$$

Typo in [Lecture 11](https://math.nyu.edu/~kleeman/infolect11.pdf), Section 2: $p(x(t) \mid y(t))$ should be $p(x(t) \mid y(t_0))$.

Having less uncertainty in one place can improve uncertainty in another area.

But it does not mean causation. There could be correlation but it may not be causation: nearby spatial variables can be correlated, so TLMI can be high.

Quote: "We shall refer to I(X(t); Y(t0)) henceforth as the 'time lagged mutual information' or TLMI. The TLMI does not measure the information flow into X from other random variables" ([Lecture 11](https://math.nyu.edu/~kleeman/infolect11.pdf), Section 2).


## Transfer entropy

Entropy of $x_t$ after knowing the $x$ history, minus entropy of $x_t$ after knowing the $x$ history and the $y$ history:

$$
T_{Y \to X} = H(x_t \mid x_{t-1}, \dots, x_{t-l}) - H(x_t \mid x_{t-1}, \dots, x_{t-l}, y_{t-1}, \dots, y_{t-l})
$$

If there is no information flow from one to the other, then conditionally $x(t)$ does not depend on $y(t_0)$:

$$
p(x(t) \mid x(t_0)) = p(x(t) \mid x(t_0), y(t_0))
$$

Quote: "Schreiber suggests using the deviation from this property as a measure of the information flow from Y into X. We can use the relative entropy of the two distributions as such a measure." ([Lecture 11](https://math.nyu.edu/~kleeman/infolect11.pdf), Section 2; Schreiber, Measuring information transfer, Phys. Rev. Lett. 85, 461 (2000).)

$$
D\big(p(x(t) \mid x(t_0), y(t_0)),\; p(x(t) \mid x(t_0))\big)
$$

We can calculate this KL divergence between the two distributions to see if they are the same or not. If KL divergence $= 0$, there is no information flow from $Y$ into $X$.

Transfer entropy is the average over everything: consider all the possible states of the conditioning variables $x(t_0), y(t_0)$. It is the expected value of the KL divergence ([Lecture 11](https://math.nyu.edu/~kleeman/infolect11.pdf), Eq. 3, first line):

$$
T(Y \to X, t, t_0) = \mathbb{E}_{x(t_0),\, y(t_0)}\Big[D\big(p(x(t) \mid x(t_0), y(t_0)),\; p(x(t) \mid x(t_0))\big)\Big]
$$

For spatially near, highly correlated $x(t_0)$ and $y(t_0)$: knowing $y(t_0)$ does not provide much information about $x(t)$ beyond that already provided by $x(t_0)$.

Transfer entropy is non-negative, because it is the expected value of KL divergence and KL divergence cannot be less than zero. It is also generally non-symmetric:

$$
T(Y \to X, t, t_0) \neq T(X \to Y, t, t_0)
$$

Analogous to the mutual information equation, it is how entropy is reduced by knowing $Y(t_0)$ ([Lecture 11](https://math.nyu.edu/~kleeman/infolect11.pdf), Section 2):

$$
T(Y \to X, t, t_0) = H(X(t) \mid X(t_0)) - H(X(t) \mid X(t_0), Y(t_0))
$$

The goal is to find the place for better observation, in such a way that we can predict things better. We can use TE or TLMI to understand this further.

Quote: "It is hoped that analyses like those shown above will have a future positive impact on deciding where to put additional elements of the observing platform which is used to initialize weather predictions." ([Lecture 11](https://math.nyu.edu/~kleeman/infolect11.pdf), Section 3.)

## Granger causality

$Y$ Granger-causes $X$ if $Y$'s past predicts $X$ better than $X$'s own past alone.

### How to calculate

Pick a lag $p$.

Restricted:

$$
x_t = \sum_{k=1}^{p} a_k x_{t-k} + e'_t
$$

Unrestricted:

$$
x_t = \sum_{k=1}^{p} a_k x_{t-k} + \sum_{k=1}^{p} b_k y_{t-k} + e_t
$$

$$
F_{y \to x} = \log \frac{\mathrm{var}(e')}{\mathrm{var}(e)}
$$

$F = 0$: $y$ does not help. $F > 0$: $y$ helps.

Noise is not measured. $e$ and $e'$ are the residuals: actual minus predicted.

```python
target = x[p:]

Xr = [x[t-1], ..., x[t-p]]                         # one row per t
e_prime = target - Xr @ least_squares(Xr, target)

Xu = [x[t-1], ..., x[t-p], y[t-1], ..., y[t-p]]
e = target - Xu @ least_squares(Xu, target)

F = log(var(e_prime) / var(e))
```

Swap $x$ and $y$ for $F_{x \to y}$.

### Notes

It only works for linear stochastic system [Need to search more to validate this claim of if DNN aided mechanism exists or not].

Quote: "Another practice is performing a Granger causality test, which is a statistical test of the usefulness of one time series in forecasting another. This kind of test, as the name implies, provides only a yes-or-no judgment, lacking the quantitative information that may be required in many circumstances." ([Liang 2014](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.90.052150), Phys. Rev. E 90, 052150.)

## Liang-Kleeman

TE and TLMI are heuristic. Quote: "The arguments given in Section 2 regarding the use of TLMI and TE as measures of uncertainty flow are essentially heuristic." ([Lecture 11](https://math.nyu.edu/~kleeman/infolect11.pdf), Section 4.)

The way to correctly find the flow is to take the entropy evolution of the marginal, minus the entropy evolution of that variable as if the causal effect of the other variable is removed (freezing of variables):

$$
\partial_t (h_1 - h_1^*)
$$

### Basis of LK equation

From [Lecture 11](https://math.nyu.edu/~kleeman/infolect11.pdf), Section 4, for a two dimensional system $p(x_1, x_2)$.

If the first component were not interacting with the second (the star is the hypothetical isolated evolution):

$$
\partial_t h_1^* = E\left(\frac{\partial A_1}{\partial x_1}\right)
$$

True evolution of $h_1$, derived from the Fokker-Planck equation (Lecture 11, Eq. 5):

$$
\partial_t h_1 = -\iint \frac{p(x_1, x_2)}{p(x_1)}\, A_1\, \frac{\partial p(x_1)}{\partial x_1}\, dx_1\, dx_2
$$

### References

- Lecture 11, Section 4: https://math.nyu.edu/~kleeman/infolect11.pdf
- Liang and Kleeman, Information transfer between dynamical system components, Phys. Rev. Lett. 95, 244101 (2005).

## TODO: Neural Granger and transfer entropy papers

- [ITENE: Intrinsic Transfer Entropy Neural Estimator](https://arxiv.org/abs/1912.07277), Zhang et al.: removes the synergistic part of transfer entropy; estimator inspired by MINE.
- [TENDE: Transfer Entropy Neural Diffusion Estimation](https://arxiv.org/abs/2510.14096), Galeano Munoz et al.: score-based diffusion models to estimate transfer entropy through conditional mutual information.
- [Neural Granger Causality](https://arxiv.org/abs/1802.05842), Tank et al.: structured MLPs or RNNs with sparsity penalties to recover Granger causal structure in nonlinear dynamics.
- [Economy Statistical Recurrent Units For Inferring Nonlinear Granger Causality](https://arxiv.org/abs/1911.09879), Khanna and Tan: lighter recurrent network; Granger causality from structured sparsity of the weights.
- [Interpretable Models for Granger Causality Using Self-explaining Neural Networks](https://arxiv.org/abs/2101.07600), Marcinkevičs and Vogt: self-explaining neural networks detect Granger causality in nonlinear time series.
