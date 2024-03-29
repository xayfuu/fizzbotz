class FizzbotzException(Exception):
    """Base exception for Fizzbotz exceptions."""


class StringLengthError(FizzbotzException):
    """String argument is too long/too short."""


class EmptyStringError(FizzbotzException):
    """String argument is empty."""
