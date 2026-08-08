"""Configuration parameters for the 2D linear SDE experiment."""

import torch

# ------------------------------------------------------------------------------
# System Dynamics Parameters (Vannitsem et al. 2019)
# ------------------------------------------------------------------------------
A11 = -1.0
A12 = 0.5
A22 = -1.0
A21 = 0.0

THEORETICAL_STEADY_STATE = 0.111111  # Expected T2->1 for this toy setup

# ------------------------------------------------------------------------------
# Simulation Parameters (EnKF)
# ------------------------------------------------------------------------------
DT = 0.1
PROCESS_NOISE_VAR = 0.01  # Continuous variance Q
OBS_NOISE_VAR = 0.02    # Observation noise R

NUM_PARTICLES = 1000       # EnKF ensemble size
BURN_IN_STEPS = 500       # Initial steps without observations
SIM_STEPS = 20000         # Number of assimilation steps

# ------------------------------------------------------------------------------
# Time-Series Experiment Parameters
# ------------------------------------------------------------------------------
TS_TOTAL_STEPS = 50000
TS_PLOT_STEP = 500

# Optional: Default tensor settings for consistency
DTYPE = torch.float32
DEVICE = "cuda"
