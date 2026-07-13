# Architecture — torch_model_deployment.py

<!-- PORTFOLIO-CONSTITUTION:START -->
## Portfolio architecture baseline

Source of truth: `docs/ARCHITECTURE.yaml`. Tracking: [Project #24](https://github.com/users/googa27/projects/24), [torch_model_deployment.py issue](https://github.com/googa27/torch_model_deployment.py/issues/1). Profile: `application`; enforcement: `Blocking`.

### Research-backed defaults

| Decision | Evidence | Repository application |
|---|---|---|
| Agent context | [Hermes context files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files), [AGENTS.md](https://agents.md/) | Root `AGENTS.md`; progressive detail stays in linked docs. |
| AI tool escalation | [MCP tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) | Stable CLI/contracts and skills first; plugin/MCP only after measured need and least-privilege review. |
| Python source layout | [PyPA src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) | Declared Python roots: `none yet`. |
| Test layout | [pytest good practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html) | Unit/integration/e2e/architecture boundaries are explicit. |
| Module budget | [Pylint too-many-lines rationale](https://pylint.readthedocs.io/en/latest/user_guide/messages/convention/too-many-lines.html) plus AI review locality | 500 physical lines is stricter than Pylint's broad default; existing excess is a no-growth ratchet. |
| Evolution | [Evolutionary architecture](https://evolutionaryarchitecture.com/precis.html) | Architecture characteristics have executable fitness functions and incremental exceptions. |
| Data layers | [Medallion architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion) | Applied only where data is consumed; simple repos record an explicit non-use decision. |
| Python protocols | [Python data model](https://docs.python.org/3/reference/datamodel.html), [NumPy dispatch](https://numpy.org/doc/stable/user/basics.dispatch.html) | Dunders express true protocols/laws; named methods own policy and effects. |

### Maintained-library decision table

| Capability | Selected route | Alternatives | Boundary / custom-code rule |
|---|---|---|---|
| Model serving demo runtime | PyTorch TorchScript 2.7.1 + FastAPI 0.116.1 + Pydantic 2.11.7 | Raw pickle/model-per-request loading; Flask ad-hoc API; custom JSON validation | `model_artifact.py` verifies manifest path containment and SHA-256 before one-time `torch.jit.load`; `api.py` owns typed DTOs and health/serve boundaries. |
| Architecture contract bootstrap | Python standard-library JSON parser over the JSON subset of YAML 1.2 | Hand-written YAML parser; mandatory platform service | Repo-local dependency-free structural gate; richer maintained tools remain repo-specific. |
| Import/dependency rules | Existing repo lint/import tools where configured; declarative YAML boundary is authoritative | Custom import framework | Keep custom AST checks narrow; use maintained Import Linter/Tach/Ruff/deptry when warranted. |
| AI interaction | AGENTS + deterministic CLI/contracts + capability discovery + skills | MCP/plugin in every repo | Escalate only after measured interoperability/lifecycle need. |

### Two-user design

- AI: AGENTS + deterministic serve/test/build commands and capability manifest; MCP not needed.
- Human/notebook: Typed inference client/model metadata API and notebook example; context manager only for real server/session lifecycle.
- Planned Python protocols: Immutable model/request/response metadata may use deterministic __repr__ and value equality.; Inference, loading, device selection, batching, network service, and persistence remain named methods.; Tensor/NumPy protocols stay framework-owned; do not wrap them with surprising custom operators.
- Core posture: Avoid finance cores; may emit generic ModelOutputBundle for UI if reused.
- Data posture: Local TorchScript artifact -> explicit manifest/SHA-256 -> verified one-time load -> typed Pydantic request -> `torch.inference_mode()` prediction -> typed response and `/health` metadata. Raw `.pkl` artifacts are removed from the serving repository.

### Serving safety boundary

The API no longer loads the model per request and never accepts a user-supplied model path or pickle bytes. `create_model.py` rebuilds the TorchScript artifact and manifest together. `model_artifact.py` fails closed on hash mismatch or path escape. Tests cover build, health, DTO validation, artifact verification, and serve behavior.

### Extension and exception discipline

Probable extensions must cross named ports/capability registries rather than adding sibling modules indefinitely. Every exception is exact, risk-bearing, no-growth, and has a refactoring trigger. Generated/vendor/migration/resource paths are declared explicitly; they do not silently weaken runtime rules.
<!-- PORTFOLIO-CONSTITUTION:END -->
