# Theoretical Model

NeuroTwin uses a three-layer model: dynamics, virtual perturbation and closed-loop experiment selection.

## 1. Brain Dynamics Surrogate

```text
x_{t+1} = F_theta(x_t, u_t, c) + epsilon_t
```

- `x_t`: ROI or network-level brain state.
- `u_t`: task stimulus, candidate intervention or context input.
- `c`: subject-level context such as connectome, phenotype or session metadata.
- `F_theta`: learned surrogate brain dynamics.

## 2. Virtual Perturbation Response

```text
R_i(x_t, delta) = F_theta(x_t + delta e_i, u_t, c) - F_theta(x_t, u_t, c)
EC_{i,j} = E_t [R_i(x_t, delta)_j]
```

This turns the trained surrogate into a virtual experimental object. Perturbing node `i` produces a response profile across target nodes.

## 3. Learn-Stage Experiment Selection

```text
a_next = argmax_a [ I(a; F_theta, D) - lambda C(a) ]
```

- `I(a; F_theta, D)`: expected information gain or uncertainty reduction from the next simulation or validation action.
- `C(a)`: validation cost, including compute, data, experimental burden and expert-review effort.
- `lambda`: cost-sensitivity parameter.

In the current demo, this is approximated by a transparent heuristic based on BOLD uncertainty, FC gap, objective signal and validation cost. A real version can replace it with Bayesian optimization, active learning or multi-objective acquisition functions.
