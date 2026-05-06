import numpy as np

from neurotwin.core import (
    NETWORKS,
    fit_surrogate,
    functional_connectivity,
    predict_surrogate,
    r2_score,
    simulate,
)


def test_simulation_shapes_are_stable() -> None:
    series, stimulus, weights = simulate("emotion", length=40, seed=13)

    assert series.shape == (40, len(NETWORKS))
    assert stimulus.shape == series.shape
    assert weights.shape == (len(NETWORKS), len(NETWORKS))
    assert np.isfinite(series).all()


def test_surrogate_prediction_and_fc_metrics_are_finite() -> None:
    series, _, _ = simulate("control", length=80, seed=17)
    coef = fit_surrogate(series)
    pred = predict_surrogate(series, coef)
    fc = functional_connectivity(series)
    score = r2_score(series, pred)

    assert pred.shape == series.shape
    assert fc.shape == (len(NETWORKS), len(NETWORKS))
    assert np.isfinite(fc).all()
    assert np.isfinite(score)
