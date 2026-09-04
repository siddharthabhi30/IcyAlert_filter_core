import torch
import config

A = torch.tensor(
    [[config.A11, config.A12], [config.A21, config.A22]],
    dtype=config.DTYPE,
)
I = torch.eye(2, dtype=config.DTYPE)
F = I + config.DT * A
Q = config.PROCESS_NOISE_VAR * config.DT * I
H = I


def kalman_covariance(P, observation_variance=config.OBS_NOISE_VAR):
    """One analytical Kalman predict/update for the existing 2D system."""
    P_forecast = F @ P @ F.T + Q
    R = observation_variance * I
    K = P_forecast @ H.T @ torch.linalg.inv(H @ P_forecast @ H.T + R)
    P_analysis = (I - K @ H) @ P_forecast
    return P_forecast, P_analysis
