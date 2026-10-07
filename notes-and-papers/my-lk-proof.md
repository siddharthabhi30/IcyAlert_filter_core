# LK derivation

Here, $P_{ij}=\mathrm{Cov}(X_i,X_j)$.

## Stochastic model

$$
\frac{dX_1}{dt}=a_{11}X_1+a_{12}X_2+\xi_1(t).
$$

$$
\frac{dX_2}{dt}=a_{22}X_2+a_{21}X_1+\xi_2(t).
$$

For these substitutions, assume $\mathrm{Cov}(X_1,\xi_1)=\mathrm{Cov}(X_2,\xi_1)=0$.

## Covariance of X1 and dX1/dt

$$
\begin{aligned}
C_{1,d1}
&=\mathrm{Cov}(X_1,\frac{dX_1}{dt}) \\
&=\mathrm{Cov}(X_1,a_{11}X_1+a_{12}X_2+\xi_1) \\
&=a_{11}\mathrm{Cov}(X_1,X_1)
 +a_{12}\mathrm{Cov}(X_1,X_2)
 +\mathrm{Cov}(X_1,\xi_1) \\
&=a_{11}P_{11}+a_{12}P_{12}.
\end{aligned}
$$

## Covariance of X2 and dX1/dt

$$
\begin{aligned}
C_{2,d1}
&=\mathrm{Cov}(X_2,\frac{dX_1}{dt}) \\
&=\mathrm{Cov}(X_2,a_{11}X_1+a_{12}X_2+\xi_1) \\
&=a_{11}\mathrm{Cov}(X_2,X_1)
 +a_{12}\mathrm{Cov}(X_2,X_2)
 +\mathrm{Cov}(X_2,\xi_1) \\
&=a_{11}P_{21}+a_{12}P_{22}.
\end{aligned}
$$

## Substitute into the LK formula

$$
T_{2\rightarrow1}
=\frac{P_{11}P_{12}C_{2,d1}-P_{12}^{2}C_{1,d1}}
{P_{11}^{2}P_{22}-P_{11}P_{12}^{2}}.
$$

Substitute the two covariance expressions:

$$
T_{2\rightarrow1}
=\frac{P_{11}P_{12}(a_{11}P_{21}+a_{12}P_{22})
-P_{12}^{2}(a_{11}P_{11}+a_{12}P_{12})}
{P_{11}^{2}P_{22}-P_{11}P_{12}^{2}}.
$$

Using $P_{21}=P_{12}$, expand the numerator:

$$
T_{2\rightarrow1}
=\frac{a_{11}P_{11}P_{12}^{2}
+a_{12}P_{11}P_{12}P_{22}
-a_{11}P_{11}P_{12}^{2}
-a_{12}P_{12}^{3}}
{P_{11}^{2}P_{22}-P_{11}P_{12}^{2}}.
$$

The two $a_{11}P_{11}P_{12}^{2}$ terms cancel. Factor the remaining numerator and denominator:

$$
T_{2\rightarrow1}
=\frac{a_{12}P_{12}(P_{11}P_{22}-P_{12}^{2})}
{P_{11}(P_{11}P_{22}-P_{12}^{2})}.
$$

Cancel the common factor:

$$
T_{2\rightarrow1}=a_{12}\frac{P_{12}}{P_{11}}.
$$

[Formula reference: Liang (2021), equation (5)](https://arxiv.org/pdf/2104.11360).

[Handwritten proof](cov-raw-proof.jpg).
