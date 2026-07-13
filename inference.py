from __future__ import annotations

from model_artifact import DoubleItModelService


model_service = DoubleItModelService.from_manifest()
ts = model_service._module  # Backward-compatible handle for older examples/tests.


if __name__ == "__main__":
    print(model_service.predict([1, 2, 3, 4]))
