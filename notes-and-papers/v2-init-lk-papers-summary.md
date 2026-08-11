## Causality-driven localization method for improving ensemble-based Kalman filters in strongly coupled data assimilation system

- **Authors:** Tian'ao Wang, Xuan Wang, Lige Cao, Wei Li, & Guijun Han (2025)
- **Link:** https://doi.org/10.3389/fmars.2025.1600634

### My understanding

They compute LK offline from a long time series and freeze the resulting causal information during data assimilation.

They use this causal information to improve the localization of the ensemble Kalman filter, instead of relying only on a fixed-radius localization.

## The dynamic causality in sporadic bursts between CO2 emission allowance prices and clean energy index

- **Authors:** Xunfa Lu, Kai Liu, Xiang San Liang, Kin Keung Lai, & Hairong Cui (2022)
- **Link:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9186288/

### My understanding

Take 250 trading days, calculate ordinary LK using covariance across those points, move the window through the daily series, and recalculate LK. The resulting curve is called dynamic causality.
