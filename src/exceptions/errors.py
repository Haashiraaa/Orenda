
# src/exceptions/errors.py

class AppError(Exception):
    """Base class for exceptions in this module."""


class EnvVariableError(AppError):
    """Raised when required environment variables are missing."""
