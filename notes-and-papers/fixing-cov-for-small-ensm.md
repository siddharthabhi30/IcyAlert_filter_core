# My Covariance Paper Notes

## Analytical Methods

### 1. EnSF-LR

EnSF-LR is just using the same update as the EnKF, with a huge number of particles: normal covariance divided by variance, similar to the EnKF update.

They call it EnSF regression, but it is just:

$$ \frac{\mathrm{Cov}(x_{\mathrm{unobs}},x_{\mathrm{obs}})}{\mathrm{Var}(x_{\mathrm{obs}})} \times \text{increment of }x_{\mathrm{obs}} $$

This happens after the forecast-to-analysis step.

- $x_{\mathrm{obs}}$ means the observed variables.
- $x_{\mathrm{unobs}}$ means the unobserved variables.

They first move the observed particles. Then they move the unobserved particles in one shot, similar to the EnKF style.

No localization is done because they tested it with only 40 dimensions. Calculating the inverse is not a concern there.

Paper: [A Two-Step Ensemble Score Filter for Data Assimilation in Partially Observed Systems](https://arxiv.org/abs/2606.28264)

---

### 2. EnSF Inpainting

First, move the observed part of the particles similarly.

Pluck out the analysis $x_posterior$ values of the observed particles and lay them out on a spatial grid.

Run an analytical image-inpainting technique. The image contains $x$ for the observed grid points and holes for the unobserved grid points.

This gives us $x_{\mathrm{unobs}}$.

Paper: [Ensemble Score Filter with Image Inpainting for Partial Observations](https://arxiv.org/abs/2501.12419)

---

### 3. LETKF

For a given state dimension $x$, LETKF gets the local observations and performs the EnKF locally. That is all: pick the local observations and correct the current state dimension.

Paper: [Efficient Data Assimilation for Spatiotemporal Chaos: A Local Ensemble Transform Kalman Filter](https://arxiv.org/abs/physics/0511236)

---

### 4. Hu and van Leeuwen, 2021

Hu and van Leeuwen do not perform the inverse of the variance of $Hx$. Instead, they use covariance between $x$ and $Hx$, divided by $R$.

They multiply the covariance matrix by a localization factor based on Gaspari–Cohn or another mechanism.

The other parts, such as doing the prior pull, are separate. If we focus on moving an unobserved variable, they use the covariance between $x$ and $Hx$.

It is simply $y-Hx$, with $H'x$ calculated for every $x$ during pseudo-moving time.

The likelihood pull is:

$$ \mathrm{Cov}\. C_{\mathrm{localization}}\. \text{innovation}\. H'x\. R^{-1} $$

Paper: [A Particle Flow Filter for High-Dimensional System Applications](https://arxiv.org/abs/1911.01511)

---

### 5. NICE and PANIC

NICE estimates how much noise is present in the sample correlation matrix. It strongly shrinks small, unreliable correlations and changes strong correlations less.

It then returns a cleaned, valid covariance matrix. That covariance can be used in an EnKF update, with additional localization if required. NICE plus localization is PANIC.

#### TODO
Understand exactly how NICE estimates the noise level and chooses its power correction. Then investigate whether a DNN can distinguish persistent weak physical correlations from accidental small-ensemble correlations.

Paper: [High-Dimensional Covariance Estimation From a Small Number of Samples](https://doi.org/10.1029/2024MS004417)

---

### 6. A Stochastic Covariance Shrinkage Approach in Ensemble Transform Kalman Filtering

What they do is:

$$ \text{Covariance matrix} = (1-y)\.\text{live covariance matrix} + y\.\text{historically collected covariance matrix} $$

Paper: [A Stochastic Covariance Shrinkage Approach in Ensemble Transform Kalman Filtering](https://arxiv.org/abs/2003.00354)

---

## DNN-Based Methods

### 7. CNN-Based Adaptive Localization

#### Convolutional Neural Network-Based Adaptive Localization for an Ensemble Kalman Filter

This is CNN-based Kalman-gain cleanup for Lorenz-05.

Run EnKFs with 40 and 2,000 ensemble members, and save the pairs of truth and prediction.

Randomly pick a time and train using MSE against the Kalman gain from 2,000 particles. That is all.

There is no autoregressive training. Simply pick a time and train the CNN.

Another version does the same thing, but instead of using the oracle, it trains using pure RMSE against the true $x$.

Again, it simply plucks a random time and trains the CNN.

Paper: [Convolutional Neural Network-Based Adaptive Localization for an Ensemble Kalman Filter](https://doi.org/10.1029/2023MS003642)

---

### 8. Machine Learning-Based Covariance Correction

#### Enabling High-Accuracy Data Assimilation with Limited Ensembles via Machine Learning-Based Covariance Correction

The algorithm is simple.

Run one filter with more particles and another with fewer particles.

Select a random time and pluck the oracle covariance and the small-ensemble covariance.

The MLP receives the small-ensemble covariance from the current time and the previous time.

The MLP has to predict the correction:

$$ \Delta = \text{oracle covariance} - \text{current small-ensemble covariance} $$

The loss is:

$$ (\Delta-\Delta_{\mathrm{MLP}})^2 $$

There is no autoregressive training. It is simple, with nothing complex.

During inference, run the filter, feed the covariance to the MLP, and obtain the corrected covariance.

Sample new particles from the corrected covariance and run the EnKF normally again. The sampling is done using the mean of the current particles because only the covariance is being corrected.

Paper: [Enabling High-Accuracy Data Assimilation with Limited Ensembles via Machine Learning-Based Covariance Correction](https://arxiv.org/abs/2605.11639)

---

# Papers to Read — TODO in Priority Order

1. [UNetKF: Machine Learning-Based Prediction of Flow-Dependent Covariance for Ensemble Data Assimilation](https://arxiv.org/abs/2403.12366)
2. [Online Machine-Learning Forecast Uncertainty Estimation for Sequential Data Assimilation (UnnKF)](https://arxiv.org/abs/2305.08874)
3. [Spectral Diagonal Ensemble Kalman Filters](https://doi.org/10.5194/npg-22-485-2015)
4. [A Shrinkage Approach to Large-Scale Covariance Matrix Estimation and Implications for Ensemble-Based Data Assimilation](https://arxiv.org/abs/1502.00301)
5. [Ensemble Kalman Filter Updates Based on Regularized Sparse Inverse Cholesky Factors](https://doi.org/10.1175/MWR-D-20-0299.1)
6. [An Adaptive Covariance Inflation Error Correction Algorithm for Ensemble Filters](https://doi.org/10.1111/j.1600-0870.2006.00216.x)
7. [Adaptive Ensemble Covariance Localization in Ensemble 4D-VAR State Estimation](https://doi.org/10.1175/2010MWR3403.1)
8. [A Hybrid Ensemble Kalman Filter–3D Variational Analysis Scheme](https://journals.ametsoc.org/view/journals/mwre/128/8/1520-0493_2000_128_2905_ahekfv_2.0.co_2.xml)
9. [Empirical Localization of Observation Impact in Ensemble Kalman Filters](https://doi.org/10.1175/MWR-D-12-00330.1)
10. [Empirical Localization Functions for Ensemble Kalman Filter Data Assimilation in Regions With and Without Precipitation](https://doi.org/10.1175/MWR-D-14-00415.1)
11. [Latent-EnSF: A Latent Ensemble Score Filter for High-Dimensional Data Assimilation With Sparse Observation Data](https://arxiv.org/abs/2409.00127)
12. [Latent Space Data Assimilation by Using Deep Learning (ETKF-Q-L)](https://arxiv.org/abs/2104.00430)
13. [Ensemble Kalman Filter in Latent Space Using a Variational Autoencoder Pair](https://arxiv.org/abs/2502.12987)
14. [LD-EnSF: Synergizing Latent Dynamics With Ensemble Score Filters for Fast Data Assimilation With Sparse Observations](https://arxiv.org/abs/2411.19305)
15. [Deep Latent Space Particle Filter](https://arxiv.org/abs/2406.02204)
16. [A Unified Neural Background-Error Covariance Model for Midlatitude and Tropical Atmospheric Data Assimilation](https://doi.org/10.1029/2025MS005360)
17. [ADAF: An Artificial Intelligence Data Assimilation Framework for Weather Forecasting](https://doi.org/10.1029/2024MS004839)
18. [CAR-EnKF: A Covariance-Adaptive and Recalibrated Ensemble Kalman Filter Framework](https://arxiv.org/abs/2604.17343)
19. [GSP-KalmanNet: Tracking Graph Signals via Neural-Aided Kalman Filtering](https://arxiv.org/abs/2311.16602)
20. [An Implementation of the Particle Flow Filter in an Atmospheric Model](https://doi.org/10.1175/MWR-D-24-0006.1)
21. [On Building the State Error Covariance From a State Estimate](https://arxiv.org/abs/2411.14809)
22. [A Review of Innovation-Based Methods to Jointly Estimate Model and Observation Error Covariance Matrices in Ensemble Data Assimilation](https://doi.org/10.1175/MWR-D-19-0240.1)
23. [Observation Error Covariance Specification in Dynamical Systems for Data Assimilation Using Recurrent Neural Networks](https://doi.org/10.1007/s00521-021-06739-4)
24. [A Scalable Real-Time Data Assimilation Framework for Predicting Turbulent Atmosphere Dynamics](https://arxiv.org/abs/2407.12168)
25. [Towards Online Real-Time Memory-Based Video Inpainting Transformers](https://openaccess.thecvf.com/content/CVPR2024W/NTIRE/html/Thiry_Towards_Online_Real-Time_Memory-based_Video_Inpainting_Transformers_CVPRW_2024_paper.html)
26. [Deep Video Inpainting](https://openaccess.thecvf.com/content_CVPR_2019/html/Kim_Deep_Video_Inpainting_CVPR_2019_paper.html)
27. [DLFormer: Discrete Latent Transformer for Video Inpainting](https://openaccess.thecvf.com/content/CVPR2022/html/Ren_DLFormer_Discrete_Latent_Transformer_for_Video_Inpainting_CVPR_2022_paper.html)
28. [ProPainter: Improving Propagation and Transformer for Video Inpainting](https://openaccess.thecvf.com/content/ICCV2023/html/Zhou_ProPainter_Improving_Propagation_and_Transformer_for_Video_Inpainting_ICCV_2023_paper.html)
29. [FourCastNet: A Global Data-Driven High-Resolution Weather Model Using Adaptive Fourier Neural Operators](https://arxiv.org/abs/2202.11214)