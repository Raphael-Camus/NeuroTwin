# Security and Data Policy

I treat NeuroTwin as a non-clinical AI4S prototype. I do not use it for diagnosis, treatment planning, or patient-specific medical decisions.

## Sensitive Data

I do not commit:

- identifiable neuroimaging data;
- DICOM/NIfTI files derived from real subjects;
- clinical notes, diagnoses, hospital identifiers, or contact information;
- dataset credentials, tokens, or private API keys.

Local experiments should use ignored folders such as `data/raw/`, `data/processed/`, and `artifacts/`.

## Reporting

If you find a privacy or data-handling problem, contact the repository owner privately. Do not open a public issue containing sensitive data.
