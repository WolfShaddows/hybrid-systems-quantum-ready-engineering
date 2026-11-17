<!-- Purpose: Define the Granite evaluation protocol, evidence, and human-review controls. -->
# AI-assisted engineering with IBM Granite

Evaluate whether an identified Granite model helps with bounded maintenance and code explanation through local inference and human review.

- Record synthetic repository/commit, model revision, license, weight hash if applicable, runtime, quantization, hardware, parameters, prompt, and date.
- Define task acceptance criteria before inference: explanation, test proposal, seeded defect detection, documentation.
- Compare with a human/no-model baseline. Score correctness, completeness, introduced defects, time/cost, and confidence.
- Repeat prompts with recorded settings; retain permitted inputs/outputs and remove sensitive data.
- A person reviews every result. The model cannot approve or deploy changes.

| Risk | Control |
|---|---|
| Hallucination or incorrect code | Tests, independent review, verifiable reference |
| Secret leakage | Synthetic data and least necessary access |
| Model revision changes | Record identifier/hash and repeat |
| Evaluation bias | Predefined criteria, balanced tasks, baseline, blind review |
| License/provenance | Record model card and obligations |

See [IBM Granite](https://www.ibm.com/granite/docs/models/granite4-0) and [SOURCES.md](../../references/SOURCES.md). Local suitability depends on the artifact/runtime; privacy is not assumed.
