# 2. Formalism: The Mathematics of the DSVL Engine

To formalize the DSVL, we define the NeuroTwin surrogate not merely as a fitting function, but as an **Automated Scientific Discovery Engine** driven by massive, high-frequency perturbation loops.

## 2.1 The Surrogate Dynamics (孪生动力学系统)
Let the state of the target neural system at time $t$ be represented by a state vector $S_t \in \mathcal{S}$. We define an external intervention or perturbation (e.g., stimulation parameters, virtual drug dosing) as $U_t \in \mathcal{U}$.

The Surrogate Brain is a physics-informed model $\mathcal{F}_{\theta}$ parameterized by $\theta$, which predicts the temporal evolution of the system:
$$ S_{t+1} = \mathcal{F}_{\theta}(S_t, U_t) + \epsilon $$
where $\epsilon \sim \mathcal{N}(0, \Sigma)$ represents the epistemic and aleatoric uncertainties inherent in complex biological systems.

## 2.2 The Discovery-Driven Objective (发现驱动的目标函数)
Unlike traditional engineering tasks with a fixed target, AI4S focuses on **open-ended discovery**. The goal of the massive perturbation loop is to uncover hidden scientific value (e.g., unknown critical phase transitions, novel biomarkers) through iterative simulation.

We formulate this as maximizing a **Scientific Utility Function**, $\mathcal{J}(U)$. Instead of purely minimizing a known error, the DSVL utilizes a Bayesian Optimization (BO) framework with a custom Acquisition Function, $\alpha(U)$, designed to balance three terms:

$$ U_{n+1}^* = \arg\max_{U \in \mathcal{U}} \Big( \underbrace{\mu_n(U)}_{\text{Exploitation}} + \lambda_1 \underbrace{\sigma_n(U)}_{\text{Exploration}} + \lambda_2 \underbrace{\mathcal{V}_{\text{Agent}}(S_{U})}_{\text{Novelty / Value}} \Big) $$

Where:
*   $\mu_n(U)$: The expected clinical/engineering outcome (Exploitation of known good regions).
*   $\sigma_n(U)$: The predictive variance or uncertainty. By maximizing this, the system is forced to **explore highly unknown perturbation spaces**, preventing it from trapping in local optima.
*   $\mathcal{V}_{\text{Agent}}(S_{U})$: The **Agent-Assigned Scientific Value**. This is the core of NeuroTwin. An LLM agent acts as a scientific critic, evaluating the simulated trajectory $S_{U}$ and assigning a high scalar value to "anomalous but biologically plausible" states, guiding the loop toward valuable scientific discoveries.

Through thousands of these virtual cycles ($n \to \infty$), the DSVL shifts from passive simulation to active scientific mining.
