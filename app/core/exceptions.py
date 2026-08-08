class UnsupportedLanguageException(Exception):
    """Raised when a requested target language generator strategy is not found."""
    pass

class InvalidStepException(Exception):
    """Raised when an automation step contains invalid or missing parameter data."""
    pass
