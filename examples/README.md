# Examples

I keep only small curated examples here. Full dashboards, complete payloads, and generated validation artifacts stay under `artifacts/` and are ignored.

- `workflow_snapshot.json`: compact machine-readable proof that the DSVL run produces metrics, ledger state, and next actions.
- `workflow_snapshot.md`: human-readable version of the same snapshot.

Regenerate both files with:

```bash
python scripts/export_workflow_snapshot.py
```
