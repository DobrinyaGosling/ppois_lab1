"""Simple identity provider."""

import secrets
from src.application.interfaces.services import IdentityProviderPort


class SimpleIdentityProvider(IdentityProviderPort):
    """Generates incremental ids."""

    def __init__(self) -> None:
        self.identity_counters: dict[str, str] = {}

    def generate_id(self, prefix: str) -> str:
        value = secrets.token_hex(6)
        self.identity_counters.setdefault(prefix, value)
        return f"{prefix}-{value}"
