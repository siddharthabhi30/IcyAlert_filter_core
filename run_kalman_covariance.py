import matplotlib.pyplot as plt
import torch
import config
from kalman_covariance import F, Q, kalman_covariance

R_VALUES = [0.005, 0.02, 0.1, 0.5, 2.0]
STEPS = 300

truth_P = torch.eye(2, dtype=config.DTYPE)
truth = []
for _ in range(STEPS):
    truth_P = F @ truth_P @ F.T + Q
    truth.append((config.A12 * truth_P[0, 1] / truth_P[0, 0]).item())

fig, ax = plt.subplots(figsize=(9, 5))
for R in R_VALUES:
    P = torch.eye(2, dtype=config.DTYPE)
    history = []
    for _ in range(STEPS):
        _, P = kalman_covariance(P, R)
        history.append((config.A12 * P[0, 1] / P[0, 0]).item())
    ax.plot(history, label=f"R={R}")

ax.plot(truth, "k--", linewidth=2, label="process-only truth")
ax.set_ylabel("$T_{2\\to1}(t)$")
ax.set_xlabel("step")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("kalman_t21_vs_R.png", dpi=150)
