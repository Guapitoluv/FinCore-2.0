from fincore.application.factories.resolvers.base import ChildResolver
from fincore.application.parsers.vault_value_parser import VaultValueParser
from fincore.domain.entities.vault import Vault
from fincore.domain.value_objects.money import Money
from fincore.domain.value_objects.scaled_money import ScaledMoney


class VaultChildResolver(ChildResolver):
    def __init__(self, value_parser: VaultValueParser) -> None:
        self._value_parser: VaultValueParser = value_parser
    
    
    def supports(self, parent: object) -> bool:
        return isinstance(parent, Vault)
    
    
    def resolve(self, literal: str) -> Money | ScaledMoney | Vault:
        try:
            return self._value_parser.parse(literal)
        except ValueError:
            return Vault(literal)