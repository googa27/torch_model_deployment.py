# AGENTS.md — torch_model_deployment.py

## Purpose and safety

`torch_model_deployment.py` is classified as `ML Deployment Demo` under Portfolio Project #24. Preserve public/upstream compatibility, privacy, and evidence boundaries; do not infer maturity beyond executable tests.

## Canonical documentation

- `README.md` where present
- `docs/ARCHITECTURE.yaml` — machine-readable source of truth
- `docs/ARCHITECTURE.md` — rationale and extension guidance

<!-- PORTFOLIO-CONSTITUTION:START -->
## Portfolio engineering constitution

This repository follows [Portfolio Project #24](https://github.com/users/googa27/projects/24) and [torch_model_deployment.py rollout issue](https://github.com/googa27/torch_model_deployment.py/issues/1). A repository-specific, evidence-backed exception in `docs/ARCHITECTURE.yaml` may specialize a rule; undocumented drift is not an exception.

### Research and maintained-library preference

- Research domain theory, maintained libraries, standards, interfaces, datasets, licenses, adjacent repositories, and probable extension paths before design or implementation.
- **Maintained-library preference:** use well-maintained libraries for solved algorithms, protocols, parsers, persistence, orchestration, dataframes, numerical methods, and security controls instead of implementing them from scratch. Record capability, selected library, alternatives, maintenance/API/license evidence, adapter boundary, and any custom-code justification.
- Custom code belongs to domain semantics, composition, adapters/contracts, or genuinely missing algorithms and must be tested against an oracle/reference.
- Turn reusable findings into maintained Hermes skills and concise support files. Add a plugin or MCP server only when stable CLI/contracts have multiple measured consumers or real interoperable external-tool needs.

### Clean and evolutionary architecture

After the dependency route is sound, apply SOLID, DRY knowledge ownership, suitable design patterns, explicit dependencies, low coupling, cohesive modules, extensibility, maintainability, and technical-debt minimization. Design for probable extensions, not speculative frameworks. Every meaningful change reduces named debt or adds an executable fitness function.

`docs/ARCHITECTURE.yaml` is the machine-readable source of truth. Update it in the same change as architecture, public API, test, CI, data, AI-interface, or exception changes.

- At each Python `src/` level, count immediate runtime `.py` files and package directories, excluding `__init__.py` and architecture/readme/typing metadata. Default maximum: 10. Deepen hierarchy around stable responsibilities instead of widening it.
- Default Python module maximum: 500 physical lines. Larger legacy files are exact no-growth exceptions with reason, owner/context, risk, accepted ceiling, and refactoring trigger.
- Keep `tests/unit`, `tests/integration`, `tests/e2e`, and `tests/architecture`; mirror source where useful. Empty suites document their intended boundary and activation trigger.
- Architecture tests enforce the YAML contract, source fan-out, module-size ratchets, exception metadata, required docs/suites, and repository-specific import/public-API rules.

### Two first-class users

1. **Hermes Agent and compatible agents:** this concise root file, deterministic CLI/public contracts, exact verification commands, and capability discovery are the baseline. Skills encode recurring procedures. Plugins/MCP are optional escalation layers, never substitutes for a stable public interface; mutation tools must be explicit, typed, least-privileged, and separately verifiable.
2. **Human programmer/notebook user:** provide a typed, documented importable API independent of CLI/UI internals and deterministic public-synthetic notebook examples where the repository is a library. Use only lawful Python protocols: compact `__repr__`, value equality/hash for deeply immutable objects, true collection/context/NumPy protocols, and pure IPython display hooks. Prefer named methods for policy, configuration, I/O, diagnostics, expensive/stateful behavior, or ambiguous mathematics. Test every claimed algebraic law and named-method/operator parity.

### Data and core-repository boundaries

For data-consuming work, design `source registry -> typed acquisition -> immutable Bronze -> canonical Silver -> curated Gold/features -> formulation/model -> governed output -> read-only UI/API/notebook` before implementation. Record grain, units, classification, lineage, quality, freshness/vintage/effective time, identity, replay, and validation.

- `PDP` owns reusable/public data acquisition and products.
- `financial_problem_formulations` owns general problem/formulation/formula/workflow semantics.
- `ui_and_artifacts` owns reusable audience-aware rendering and artifact QA.
- Consume stable public contracts/CLIs, not repository internals. Keep canonical names theoretical/general rather than deal/product-specific.

Repository posture: Avoid finance cores; may emit generic ModelOutputBundle for UI if reused. Data posture: Model/data artifacts need provenance, hashes, classification, and reproducible build/serve boundary.

### Exact commands

- Setup: `python -m pip install -r requirements.txt`
- Tests: `python -m pytest -q`
- Lint/format: `ruff check .`
- Portfolio architecture: `python scripts/check_portfolio_architecture.py`

If a command is declared unavailable, the activation trigger and replacement command belong in `docs/ARCHITECTURE.yaml`; do not fabricate successful output.
<!-- PORTFOLIO-CONSTITUTION:END -->
