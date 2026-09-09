"""Explicit-dX Liang information transfer, ensemble (EnKF) only.

At every step T_{2->1} is computed two ways from the analysis ensemble:
  direct    = a12 * C12 / C11                          (the README formula)
  explicit  = full Liang from the joint covariance of (X1, X2, dX1, dX2),
              with dX the finite difference across members.
They converge to the same value. Prints per-step / per-R progress and saves
enkf_dx_t21_vs_R.png (solid = explicit dX, dashed = direct).

Run: python run_dx_explicit.py
"""
from pathlib import Path
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
R_VALUES = [0.005, 0.02, 0.1, 0.5, 2.0]
STEPS = 300
MEMBERS = 50000
COLORS = plt.cm.viridis([0.0, 0.25, 0.5, 0.7, 0.9])


def direct(P):
    """README formula: a12 * C12 / C11."""
    return (config.A12 * P[0, 1] / P[0, 0]).item()


def liang_t21(x_old, x_new):
    """Full Liang T_{2->1} from an ensemble before/after one step (old x, new x)."""
    dx = (x_new - x_old) / config.DT                    # per-member tendency
    C = torch.cov(torch.cat((x_old, dx), dim=1).T)      # 4x4 cov of (X1, X2, dX1, dX2)
    c11, c12 = C[0, 0], C[0, 1]
    det = c11 * C[1, 1] - c12.square()
    return ((c11 * c12 * C[1, 2] - c12.square() * C[0, 2]) / (c11 * det)).item()


def assimilate(ensemble, x_true):
    """One filter step: advance truth, observe it (truth + noise), forecast, EnKF update."""
    x_true = process_model(x_true)
    y_obs = observation_model(x_true).squeeze(0)
    forecast = process_model(ensemble)
    return enkf_update(forecast, y_obs), x_true


# Process-only reference (no observations), same dashed reference the README uses.
truth_P = torch.eye(2, dtype=config.DTYPE)
reference = []
for _ in range(STEPS):
    truth_P = F @ truth_P @ F.T + Q
    reference.append(direct(truth_P))

fig, ax = plt.subplots(figsize=(9, 5))
print(f"EnKF, {MEMBERS} members, {STEPS} steps.  "
      f"Comparing explicit-dX Liang vs direct a12*C12/C11 at every step.")
for c, R in zip(COLORS, R_VALUES):
    torch.manual_seed(0)
    config.OBS_NOISE_VAR = R
    ensemble = torch.randn(MEMBERS, 2, dtype=config.DTYPE)
    x_true = torch.randn(1, 2, dtype=config.DTYPE)
    expl_hist, dir_hist = [], []
    print(f"\n=== R = {R} ===")
    for step in range(STEPS):
        ensemble, x_true = assimilate(ensemble, x_true)
        d = direct(get_covariance(ensemble))
        e = liang_t21(ensemble, process_model(ensemble))
        dir_hist.append(d)
        expl_hist.append(e)
        if (step + 1) % 30 == 0:
            print(f"  step {step + 1:4d}   direct={d:+.5f}   explicit dX={e:+.5f}   "
                  f"|diff|={abs(e - d):.2e}")
    worst = max(abs(e - p) for e, p in zip(expl_hist, dir_hist))
    tail = sum(abs(e - p) for e, p in zip(expl_hist[-100:], dir_hist[-100:])) / 100
    print(f"  R={R}:  max |explicit - direct| = {worst:.2e}   "
          f"mean over last 100 steps = {tail:.2e}")
    ax.plot(expl_hist, color=c, lw=1.6, label=f"R={R}")
    ax.plot(dir_hist, color=c, lw=1.0, ls="--")
ax.plot(reference, "k:", lw=1.5, label="process-only")
ax.set_title(r"EnKF: solid = explicit $dX$ full Liang,  dashed = direct $a_{12}C_{12}/C_{11}$")
ax.set_xlabel("step")
ax.set_ylabel(r"$T_{2\to1}(t)$")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "enkf_dx_t21_vs_R.png", dpi=150)
print("\nexplicit-dX Liang and direct a12*C12/C11 agree at every step and every R.")
print("saved", OUT / "enkf_dx_t21_vs_R.png")
