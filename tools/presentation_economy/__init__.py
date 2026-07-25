"""Strict, tool-local presentation economy data contracts."""

from .validation import (
    ValidationError,
    load_dataset,
    load_workload,
    validate_dataset,
    validate_workload,
)
from .comparison import build_comparison

__all__ = [
    "ValidationError",
    "load_dataset",
    "load_workload",
    "validate_dataset",
    "validate_workload",
    "build_comparison",
]
