from typing import Callable

from fincore.application.parsers.base import VaultValueParser
from fincore.domain.value_objects.money import Money
from fincore.domain.value_objects.scaled_money import ScaledMoney
from fincore.domain.entities.vault import Vault


class DefaultVaultValueParser(VaultValueParser):
    def __init__(
            self,
            strategies: list[Callable[[str], Money | ScaledMoney | Vault]]
        ) -> None:
        
        self._strategies: list[Callable[[str], Money | ScaledMoney | Vault]] = strategies
    
    
    def parse(self, literal: str) -> Money | ScaledMoney | Vault:

        errors = []

        for strategy in self._strategies:
            try:
                return strategy(literal)
            except ValueError as e:
                errors.append(str(e))

        raise ValueError(
            f"Invalid vault value: '{literal}'"
        )