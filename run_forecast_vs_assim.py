"""Forecast vs assimilated T_{2->1}, single noise level.

The ensemble IS assimilated every step (EnKF update runs normally). But we read
T_{2->1} off two covariances and compare them:
  forecast    = a12 * C12/C11 from the forecast covariance   (before the update)
  assimilated = a12 * C12/C11 from the analysis covariance    (after the update)

Prints both per step and saves forecast_vs_assim_t21.png.
Run: python run_forecast_vs_assim.py
"""
from pathlib import Path
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config
from process_model import process_model
from observation_model import observation_model
from enKF import enkf_update, get_covariance
from kalman_covariance import F, Q

OUT = Path(__file__).resolve().parent
R = 0.05
STEPS = 300
MEMBERS = 50000
torch.manual_seed(0)
config.OBS_NOISE_VAR = R


def t21(P):
    return (config.A12 * P[0, 1] / P[0, 0]).item()


# Process-only reference (no observations).
truth_P = torch.eye(2, dtype=config.DTYPE)
reference = []
for _ in range(STEPS):
    truth_P = F @ truth_P @ F.T + Q
    reference.append(t21(truth_P))

ensemble = torch.randn(MEMBERS, 2, dtype=config.DTYPE)
x_true = torch.randn(1, 2, dtype=config.DTYPE)
fc_hist, an_hist = [], []
print(f"R = {R},  {MEMBERS} members.  Ensemble is assimilated every step;")
print("printing forecast T21 (before update) vs assimilated T21 (after update).")
for step in range(STEPS):
    x_true = process_model(x_true)
    y_obs = observation_model(x_true).squeeze(0)                           # truth + observation noise
    forecast = process_model(ensemble)
    t_fc = t21(get_covariance(forecast))                                   # before assimilation
    ensemble = enkf_update(forecast, y_obs)                                # assimilation happens
    t_an = t21(get_covariance(ensemble))                                   # after assimilation
    fc_hist.append(t_fc)
    an_hist.append(t_an)
    if (step + 1) % 20 == 0:
        print(f"  step {step + 1:4d}   forecast T21={t_fc:+.5f}   assimilated T21={t_an:+.5f}")

print(f"\nsteady (last 100 steps):  forecast={np.mean(fc_hist[-100:]):.4f}   "
      f"assimilated={np.mean(an_hist[-100:]):.4f}   reference={reference[-1]:.4f}")

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(fc_hist, color="tab:blue", lw=1.6, label="forecast T21 (before assimilation)")
ax.plot(an_hist, color="tab:red", lw=1.6, label="assimilated T21 (after assimilation)")
ax.plot(reference, "k--", lw=1.2, label="process-only reference")
ax.set_title(rf"Forecast vs assimilated $T_{{2\to1}}$   (R={R})")
ax.set_xlabel("step")
ax.set_ylabel(r"$T_{2\to1}(t)$")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "forecast_vs_assim_t21.png", dpi=150)
print("saved", OUT / "forecast_vs_assim_t21.png")
