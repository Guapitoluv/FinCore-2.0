from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class OperationKind(str, Enum):
    ASSIGN = "assign"
    ADD = "add"
    SUB = "sub"
    REKEY = "rekey"
    DELETE = "delete"
    SELECT = "select"
    GROUP_CREATE = "group_create"


@dataclass(frozen=True)
class InstructionPath:
    segments: list[str]


@dataclass(frozen=True)
class InstructionOperation:
    kind: OperationKind
    operands: list[str | int] = field(default_factory=list)


@dataclass(frozen=True)
class AnalyzedInstruction:
    path: InstructionPath
    operation: InstructionOperation