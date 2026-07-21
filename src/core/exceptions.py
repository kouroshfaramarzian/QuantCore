"""
Custom exceptions for QuantCore.
"""


class QuantCoreError(Exception):
    """Base exception for QuantCore."""
    pass


class ConfigurationError(QuantCoreError):
    """Configuration related errors."""
    pass


class EnvironmentError(QuantCoreError):
    """Environment variable errors."""
    pass


class DataError(QuantCoreError):
    """Dataset related errors."""
    pass


class ModelError(QuantCoreError):
    """Model related errors."""
    pass


class PredictionError(QuantCoreError):
    """Prediction related errors."""
    pass