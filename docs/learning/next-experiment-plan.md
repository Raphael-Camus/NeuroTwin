# Next Experiment Plan

This plan turns the virtual perturbation demo into an executable dry-run workflow that can later be connected to public fMRI data or laboratory feedback.

## Emotional faces

- Hypothesis: Visual-to-limbic over-response can be reduced by strengthening top-down control.
- Dry run: Replay emotional-face task fMRI with subject-level train/test split.
- Human or experiment check: Compare simulated limbic reduction with task accuracy, reaction time and expert ROI review.
- Success gate: BOLD R2 > 0.70, FC corr > 0.75, perturbation direction stable across 3 seeds.
- Learn-stage priority: Behavior endpoint alignment (score 0.2037)
- Review-gate validation: OpenNeuro BIDS smoke test -> Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated.

## Cognitive control

- Hypothesis: Frontoparietal reinforcement and default-mode suppression improve conflict-task stability.
- Dry run: Run cognitive-control task simulation under multiple perturbation strengths.
- Human or experiment check: Validate against Stroop-like behavior labels or reaction-time shift.
- Success gate: Control gain positive, default-mode intrusion reduced, no large visual-network degradation.
- Learn-stage priority: Behavior endpoint alignment (score 0.1112)
- Review-gate validation: OpenNeuro BIDS smoke test -> Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated.

## Closed-loop neuro experiment

- Hypothesis: A small network-level perturbation can move salience/subcortical dynamics toward a stable attractor.
- Dry run: Search perturbation scale with objective/cost trade-off and uncertainty logging.
- Human or experiment check: Route top candidate to neurofeedback, stimulation planning, organoid readout, or clinician review.
- Success gate: Objective improves under constrained perturbation and remains robust to missing ROI masking.
- Learn-stage priority: Constrained policy search (score 0.1671)
- Review-gate validation: OpenNeuro BIDS smoke test -> Pipeline completes, BOLD R2 and FC corr are recorded, review status is updated.
