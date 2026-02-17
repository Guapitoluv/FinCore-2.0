from __future__ import annotations
from dataclasses import dataclass
from typing import TypeAlias, Sequence, Self


@dataclass(frozen=True)
class MoneyDTO:
    reais: int
    centavos: int


@dataclass(frozen=True)
class ScaledMoneyDTO:
    money: MoneyDTO
    factor: int


@dataclass(frozen=True)
class VaultDTO:
    id: str
    name: str
    vaults: dict[str, "VaultDTO"]
    values: list[MoneyDTO | ScaledMoneyDTO]


@dataclass(frozen=True)
class PersonDTO:
    id: str
    name: str
    vaults: dict[str, VaultDTO]


@dataclass(frozen=True)
class GroupDTO:
    id: str
    name: str
    members: dict[str, PersonDTO]


@dataclass(frozen=True)
class GroupAggregateDTO:
    groups: dict[str, GroupDTO]