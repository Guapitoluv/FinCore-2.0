from typing import Any

from fincore.application.cli.instruction_dtos import (
    AnalyzedInstruction,
    InstructionOperation,
    InstructionPath,
    OperationKind
)
from fincore.application.cli.instruction_grammar import (
    DELETE,
    REKEY,
    ASSIGN,
    ADD,
    SUB,
    SELECT
)
from fincore.application.cli.raw_instruction import RawInstruction
from fincore.shared.strings import remove_substring


def parse_path(path: str) -> InstructionPath:
    return InstructionPath(
        segments=path.split(".")
    )


def parse_add_group_instruction(raw_instruction: RawInstruction) -> AnalyzedInstruction:
    path: str = raw_instruction.removesuffix(DELETE)
    
    return AnalyzedInstruction(
        path=parse_path(path)
    )


def parse_delete_instruction(raw_instruction: RawInstruction) -> AnalyzedInstruction:
    path: str = raw_instruction.removesuffix(DELETE)
    
    return AnalyzedInstruction(
        path=parse_path(path),
        operation=InstructionOperation(kind=OperationKind.DELETE)
    )


def parse_rekey_instruction(raw_instruction: RawInstruction) -> AnalyzedInstruction:
    path, new = raw_instruction.split_once(REKEY)
    
    instruction_operation: InstructionOperation = InstructionOperation(
        kind=OperationKind.REKEY,
        operands=[new.strip()]
    )
    
    return AnalyzedInstruction(
        path=parse_path(path.strip()),
        operation=instruction_operation
    )


def parse_int(value: Any) -> int:
    try:
        return int(value)
    except:
        raise ValueError(f"Invalid integer literal: '{value}'")


def parse_operation(expr: str) -> InstructionOperation:
    expr = expr.strip()

    if ADD in expr:
        left, right = map(str.strip, expr.split(ADD, 1))
        return InstructionOperation(
            kind=OperationKind.ADD,
            operands=[parse_int(left), parse_int(right)]
        )

    if SUB in expr[1:]:
        left, right = map(str.strip, expr.split(SUB, 1))
        return InstructionOperation(
            kind=OperationKind.SUB,
            operands=[parse_int(left), parse_int(right)]
        )

    try:
        return InstructionOperation(
            kind=OperationKind.ASSIGN,
            operands=[parse_int(expr)]
        )
    except ValueError:
        return InstructionOperation(
            kind=OperationKind.ASSIGN,
            operands=[expr]
        )


def parse_assign_instruction(raw_instruction: RawInstruction) -> AnalyzedInstruction:
    path, expr = raw_instruction.split_once(ASSIGN)
    
    return AnalyzedInstruction(
        path=parse_path(path.strip()),
        operation=(
            InstructionOperation(
                OperationKind.GROUP_CREATE,
                [expr.strip()]
            )
            if path.strip() == "groups" else
            parse_operation(expr.strip())
        )
    )


def parse_select_instruction(raw_instruction: RawInstruction) -> AnalyzedInstruction:
    path: str = raw_instruction.removesuffix(SELECT, normalize=True)
    
    return AnalyzedInstruction(
        path=parse_path(path.strip()),
        operation=InstructionOperation(kind=OperationKind.SELECT)
    )