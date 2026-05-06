# NeuroTwin Workflow Snapshot

I keep this small snapshot in Git to show that NeuroTwin produces concrete metrics, gates, and next actions. The larger dashboard and full JSON payload remain generated artifacts.

| Scenario | BOLD R2 | FC Corr | Objective Delta | Readiness | Top Next Action |
| --- | ---: | ---: | ---: | ---: | --- |
| Emotional faces | 0.8387 | 0.8980 | 0.3587 | 0.88 | Behavior endpoint alignment |
| Cognitive control | 0.8593 | 0.9416 | 0.1031 | 0.88 | Behavior endpoint alignment |
| Closed-loop neuro experiment | 0.7382 | 0.9396 | 0.1762 | 0.88 | Constrained policy search |

Contract checks included in this snapshot:

- scenario metrics are present
- validation ledger gates are present
- review queue is present
- ranked next actions are present
- next validation packets list required outputs
