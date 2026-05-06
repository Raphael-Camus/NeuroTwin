# Mathematical Frame

I keep the current math intentionally lightweight. The goal is to make the DSVL contract inspectable before I add heavier models.

## Surrogate Dynamics

I represent the brain-network state at time `t` as an ROI or network vector:

```text
x_t in R^N
```

The baseline surrogate learns a one-step transition:

```text
x_(t+1) = f_theta(x_t)
```

In the demo, `f_theta` is a ridge-regularized linear one-step model. I chose this baseline because it is transparent, fast, and enough to test the workflow. Later versions can replace it with a graph temporal network, latent dynamics model, neural ODE, or subject-aware hypernetwork.

## Virtual Perturbation

After fitting the surrogate, I perturb each source dimension and measure the average response:

```text
EC[i, j] = mean_t f_theta(x_t + delta * e_i)[j] - f_theta(x_t)[j]
```

I treat this as a virtual effective-connectivity estimate, not as biological ground truth. It is a way to ask how the fitted surrogate responds under controlled counterfactual changes.

## Acquisition Score

The Learn stage ranks the next action using transparent terms:

```text
priority = expected_information_gain - lambda * validation_cost
```

I also track a multi-objective portfolio:

- fidelity gain;
- objective alignment;
- novelty;
- feasibility;
- risk control.

This gives me a readable policy before I introduce Bayesian optimization.
