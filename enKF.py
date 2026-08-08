import torch
import config


def enkf_update(x_forecast: torch.Tensor, y_obs: torch.Tensor) -> torch.Tensor:
    """
    Stochastic EnKF update step.

    Args:
        x_forecast: Forecast ensemble. Shape: (N, 2)
        y_obs: The actual observation received. Shape: (2,)
        
    Returns:
        Analysis ensemble (updated members). Shape: (N, 2)
    """
    N, state_dim = x_forecast.shape
    
    # Independent observation errors: R = observation variance * I.
    R_cov = config.OBS_NOISE_VAR * torch.eye(
        state_dim,
        dtype=x_forecast.dtype,
        device=x_forecast.device,
    )
    obs_std = torch.sqrt(torch.tensor(
        config.OBS_NOISE_VAR,
        dtype=x_forecast.dtype,
        device=x_forecast.device,
    ))
    
    # Forecast sample covariance P.
    x_mean = x_forecast.mean(dim=0, keepdim=True)
    anomalies = x_forecast - x_mean
    P = (anomalies.T @ anomalies) / (N - 1)
    
    # H = I here, so K = P(P + R)^-1.
    K = P @ torch.linalg.inv(P + R_cov)
    
    # Perturb every observation with noise sampled from N(0, R).
    perturbed_y = y_obs + torch.randn_like(x_forecast) * obs_std
    
    # 4. Update each ensemble member
    innovations = perturbed_y - x_forecast
    x_analysis = x_forecast + innovations @ K.T
    
    return x_analysis.detach()


def get_covariance(x_ensemble: torch.Tensor) -> torch.Tensor:
    """
    Helper to extract the covariance of an ensemble.
    """
    N = x_ensemble.shape[0]
    x_mean = x_ensemble.mean(dim=0, keepdim=True)
    anomalies = x_ensemble - x_mean
    return (anomalies.T @ anomalies) / (N - 1)
