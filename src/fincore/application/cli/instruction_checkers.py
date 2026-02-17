from fincore.application.cli.instruction_grammar import (
    ASSIGN,
    DELETE,
    REKEY,
    SELECT
)
from fincore.shared.strings import remove_substrings


def is_delete_instruction(normalized: str) -> bool:
    return normalized.endswith(DELETE)


def is_rekey_instruction(normalized: str) -> bool:
    return REKEY in normalized


def is_assign_instruction(normalized: str) -> bool:
    return ASSIGN in normalized


def is_select_instruction(normalized: str) -> bool:
    return normalized.endswith(SELECT)


def is_path_syntax(normalized: str) -> bool:
    return remove_substrings(normalized, ".", "_").isalnum()