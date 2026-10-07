# LK derivation

Here, $u_1$ and $u_2$ are the means of $X_1$ and $X_2$, and $P_{ij}=\operatorname{Cov}(X_i,X_j)$.

## Stochastic model

$$
\frac{dX_1}{dt}=a_{11}X_1+a_{12}X_2+\xi_1(t).
$$

$$
\frac{dX_2}{dt}=a_{22}X_2+a_{21}X_1+\xi_2(t).
$$

Here, $\xi_1(t)$ and $\xi_2(t)$ are the process-noise terms.

## Covariances

$$
C_{2,d1}=a_{11}P_{21}+a_{12}P_{22}.
$$

$$
C_{1,d1}=a_{11}P_{11}+a_{12}P_{12}.
$$

## Starting formula

$$
T_{2\rightarrow1}
=\frac{P_{11}P_{12}C_{2,d1}-P_{12}^{2}C_{1,d1}}
{P_{11}^{2}P_{22}-P_{11}P_{12}^{2}}.
$$

[Formula reference: Liang (2021), equation (5)](https://arxiv.org/pdf/2104.11360).

## Expansion and cancellation

First, substitute into the first numerator term:

$$
P_{11}P_{12}\left(a_{11}P_{21}+a_{12}P_{22}\right).
$$

Using $P_{21}=P_{12}$, the numerator becomes:

$$
a_{11}P_{11}P_{12}^{2}
+a_{12}P_{22}P_{12}P_{11}
-a_{11}P_{12}^{2}P_{11}
-a_{21}P_{12}^{3}.
$$

The two $a_{11}P_{11}P_{12}^{2}$ terms cancel.

Factoring:

$$
\frac{(a_{21}P_{12})(P_{22}P_{11}-P_{12}^{2})}
{P_{11}(P_{22}P_{11}-P_{12}^{2})}.
$$

Cancelling the common factor:

$$
a_{21}\frac{P_{12}}{P_{11}}.
$$

[Handwritten proof](cov-raw-proof.jpg).
