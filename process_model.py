import torch
import config


def process_model(x: torch.Tensor) -> torch.Tensor:
    """
    Stochastic 2D linear system process model from Vannitsem et al. (2019).

    Input x shape: (N, 2)
    Output shape: (N, 2)
    """
    x1 = x[:, 0]  # Shape: (N,)
    x2 = x[:, 1]  # Shape: (N,)

    # Drift
    dx1_dt = config.A11 * x1 + config.A12 * x2  # Shape: (N,)
    dx2_dt = config.A22 * x2 + config.A21 * x1  # Shape: (N,)

    # Noise
    noise_std = torch.sqrt(torch.tensor(config.PROCESS_NOISE_VAR * config.DT, dtype=x.dtype, device=x.device))
    xi1 = torch.randn_like(x1) * noise_std  # Shape: (N,)
    xi2 = torch.randn_like(x2) * noise_std  # Shape: (N,)

    # Euler-Maruyama step
    x1_next = x1 + dx1_dt * config.DT + xi1  # Shape: (N,)
    x2_next = x2 + dx2_dt * config.DT + xi2  # Shape: (N,)

    x_next = torch.stack([x1_next, x2_next], dim=1)  # Shape: (N, 2)
    return x_next.detach()
