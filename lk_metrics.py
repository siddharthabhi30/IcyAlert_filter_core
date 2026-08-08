import torch
import config


def calc_T2_to_1(covariance_matrix: torch.Tensor) -> float:
    """
    Calculates the Liang-Kleeman information transfer from X2 to X1.
    T_{2->1} = a12 * P12 / P11
    
    Args:
        covariance_matrix: 2x2 covariance matrix.
        
    Returns:
        The T_{2->1} scalar value.
    """
    # P11 is var(X1)
    p11 = covariance_matrix[0, 0]
    # P12 is cov(X1, X2)
    p12 = covariance_matrix[0, 1]
    
    t_21 = config.A12 * (p12 / p11)
    
    return t_21.item()
