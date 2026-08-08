import torch
import config


def observation_model(x_state: torch.Tensor) -> torch.Tensor:
    """
    Observation model: y = Hx + v
    where H = I, and v ~ N(0, R).
    
    Input x_state shape: (2,) for a single truth state, or (N, 2) for an ensemble.
    Output y shape: Same as input.
    """
    # Standard deviation for observation noise
    obs_std = torch.sqrt(torch.tensor(config.OBS_NOISE_VAR, dtype=x_state.dtype, device=x_state.device))
    
    # Generate observation noise v ~ N(0, R)
    v = torch.randn_like(x_state) * obs_std
    
    # y = Hx + v (where H is the identity matrix)
    y = x_state + v
    
    return y.detach()
