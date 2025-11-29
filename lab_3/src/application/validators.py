
from src.errors import InvalidInputError


def ensure_not_blank(value: str, field_name: str) -> str:
    if value is None:
        raise InvalidInputError(field_name, "value is required")
    stripped = value.strip()
    if not stripped:
        raise InvalidInputError(field_name, "value cannot be blank")
    return stripped


def ensure_non_negative(value: float, field_name: str) -> float:
    if value is None:
        raise InvalidInputError(field_name, "value is required")
    if value < 0:
        raise InvalidInputError(field_name, "value must be non-negative")
    return value


def ensure_positive(value: float, field_name: str) -> float:
    if value is None:
        raise InvalidInputError(field_name, "value is required")
    if value <= 0:
        raise InvalidInputError(field_name, "value must be positive")
    return value
