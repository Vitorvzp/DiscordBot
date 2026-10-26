"""Resolve private runtime files without falling back to repository copies."""

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PREFIX = "DISCORDBOT"


def external_path(variable: str) -> Path:
    value = os.environ.get(variable)
    if not value:
        raise RuntimeError(f"Configure {variable} with an absolute path outside the checkout.")
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        raise RuntimeError(f"{variable} must be an absolute path outside the checkout.")
    candidate = candidate.resolve()
    if candidate == PROJECT_ROOT or PROJECT_ROOT in candidate.parents:
        raise RuntimeError(f"{variable} must point outside the checkout.")
    return candidate


def private_file(variable: str) -> Path:
    candidate = external_path(variable)
    if not candidate.is_file():
        raise RuntimeError(f"{variable} must point to an existing private file.")
    return candidate


def data_file(*parts: str) -> Path:
    root = external_path(f"{ENV_PREFIX}_DATA_DIR")
    candidate = root.joinpath(*parts).resolve()
    if candidate == root or root not in candidate.parents:
        raise RuntimeError("Runtime file must remain within the configured data directory.")
    if candidate == PROJECT_ROOT or PROJECT_ROOT in candidate.parents:
        raise RuntimeError("Runtime file must remain outside the checkout.")
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate
