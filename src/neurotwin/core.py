"""Minimal BrainTwin Lab demo core.

The demo intentionally uses synthetic ROI-level signals. It demonstrates a
workflow contract with no medical-model claim: data -> surrogate dynamics ->
virtual perturbation -> validation trace -> next experiment suggestion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np


NETWORKS: List[str] = [
    "Visual",
    "Attention",
    "Frontoparietal",
    "DefaultMode",
    "Limbic",
    "Salience",
    "Somatomotor",
    "Subcortical",
]


@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    drives: Dict[str, float]
    intervention: Dict[str, float]
    objective: str


SCENARIOS: Dict[str, Scenario] = {
    "emotion": Scenario(
        name="Emotional faces",
        description="Negative-valence task: visual input recruits limbic and salience circuits.",
        drives={"Visual": 0.85, "Limbic": 0.72, "Salience": 0.42},
        intervention={"Limbic": -0.42, "Frontoparietal": 0.20, "Attention": 0.12},
        objective="Lower limbic over-response while preserving visual processing.",
    ),
    "control": Scenario(
        name="Cognitive control",
        description="Conflict task: attention and frontoparietal networks coordinate response control.",
        drives={"Attention": 0.78, "Frontoparietal": 0.70, "Somatomotor": 0.40},
        intervention={"Frontoparietal": 0.32, "Attention": 0.24, "DefaultMode": -0.28},
        objective="Increase control-network stability and reduce default-mode intrusion.",
    ),
    "closed_loop": Scenario(
        name="Closed-loop neuro experiment",
        description="A dry-run policy proposes a stimulation or molecular hypothesis and re-simulates response.",
        drives={"Salience": 0.45, "Subcortical": 0.36, "Frontoparietal": 0.24},
        intervention={"Salience": -0.22, "Subcortical": -0.18, "Frontoparietal": 0.30},
        objective="Select the smallest perturbation that shifts the network toward a healthier attractor.",
    ),
}


def stable_matrix(seed: int = 7) -> np.ndarray:
    """Create a stable directed coupling matrix with interpretable motifs."""
    rng = np.random.default_rng(seed)
    n = len(NETWORKS)
    w = rng.normal(0, 0.08, size=(n, n))
    np.fill_diagonal(w, 0.22)

    def link(src: str, dst: str, value: float) -> None:
        w[NETWORKS.index(dst), NETWORKS.index(src)] += value

    link("Visual", "Limbic", 0.32)
    link("Visual", "Attention", 0.24)
    link("Limbic", "Salience", 0.28)
    link("Salience", "Frontoparietal", 0.20)
    link("Attention", "Frontoparietal", 0.22)
    link("Frontoparietal", "DefaultMode", -0.26)
    link("DefaultMode", "Attention", -0.18)
    link("Subcortical", "Limbic", 0.18)
    link("Somatomotor", "Attention", 0.12)

    radius = max(abs(np.linalg.eigvals(w)))
    return w / max(radius / 0.88, 1.0)


def stimulus_series(length: int, scenario: Scenario) -> np.ndarray:
    n = len(NETWORKS)
    stim = np.zeros((length, n))
    for start in range(8, length, 26):
        width = 7
        pulse = np.hanning(width * 2)[:width]
        for network, strength in scenario.drives.items():
            idx = NETWORKS.index(network)
            stim[start : start + width, idx] += strength * pulse[: max(0, min(width, length - start))]
    return stim


def simulate(
    scenario_key: str,
    length: int = 150,
    seed: int = 13,
    intervention_scale: float = 0.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate ROI signals under a task and optional intervention."""
    scenario = SCENARIOS[scenario_key]
    rng = np.random.default_rng(seed)
    w = stable_matrix(seed=7)
    stim = stimulus_series(length, scenario)
    x = np.zeros((length, len(NETWORKS)))
    x[0] = rng.normal(0, 0.08, len(NETWORKS))
    intervention = np.zeros(len(NETWORKS))
    for network, value in scenario.intervention.items():
        intervention[NETWORKS.index(network)] = value
    for t in range(1, length):
        noise = rng.normal(0, 0.035, len(NETWORKS))
        u = stim[t] + intervention_scale * intervention
        x[t] = 0.58 * x[t - 1] + 0.42 * np.tanh(w @ x[t - 1] + u + noise)
    return x, stim, w


def fit_surrogate(series: np.ndarray, alpha: float = 0.65) -> np.ndarray:
    """Fit a ridge one-step surrogate x(t) -> x(t+1)."""
    x_prev = series[:-1]
    y_next = series[1:]
    x_aug = np.concatenate([x_prev, np.ones((len(x_prev), 1))], axis=1)
    reg = alpha * np.eye(x_aug.shape[1])
    reg[-1, -1] = 0.0
    coef = np.linalg.solve(x_aug.T @ x_aug + reg, x_aug.T @ y_next)
    return coef


def predict_surrogate(series: np.ndarray, coef: np.ndarray) -> np.ndarray:
    x_aug = np.concatenate([series[:-1], np.ones((len(series) - 1, 1))], axis=1)
    pred = x_aug @ coef
    return np.vstack([series[0], pred])


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - y_true.mean(axis=0)) ** 2))
    return 1.0 - ss_res / ss_tot


def functional_connectivity(series: np.ndarray) -> np.ndarray:
    return np.nan_to_num(np.corrcoef(series.T), nan=0.0)


def effective_connectivity_from_surrogate(
    series: np.ndarray, coef: np.ndarray, delta: float = 0.30
) -> np.ndarray:
    """Average one-step response after perturbing each source node."""
    n = len(NETWORKS)
    base_aug = np.concatenate([series[:-1], np.ones((len(series) - 1, 1))], axis=1)
    base = base_aug @ coef
    ec = np.zeros((n, n))
    for source in range(n):
        perturbed = base_aug.copy()
        perturbed[:, source] += delta
        response = perturbed @ coef - base
        ec[source] = response.mean(axis=0)
    return ec


def summarize_candidate(pre: np.ndarray, post: np.ndarray) -> Dict[str, float]:
    idx = {name: NETWORKS.index(name) for name in NETWORKS}
    limbic_drop = float(pre[:, idx["Limbic"]].mean() - post[:, idx["Limbic"]].mean())
    control_gain = float(post[:, idx["Frontoparietal"]].mean() - pre[:, idx["Frontoparietal"]].mean())
    salience_drop = float(pre[:, idx["Salience"]].mean() - post[:, idx["Salience"]].mean())
    objective_delta = 0.45 * limbic_drop + 0.35 * control_gain + 0.20 * salience_drop
    return {
        "limbic_drop": limbic_drop,
        "control_gain": control_gain,
        "salience_drop": salience_drop,
        "objective_delta": objective_delta,
    }
