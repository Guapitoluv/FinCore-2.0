from typing import Callable

from fincore.application.cli.instruction_dtos import AnalyzedInstruction
from fincore.application.cli.raw_instruction import RawInstruction
from fincore.application.cli.instruction_parsers import (
    parse_delete_instruction,
    parse_rekey_instruction,
    parse_assign_instruction,
    parse_select_instruction
)
from fincore.application.cli.instruction_checkers import (
    is_delete_instruction,
    is_rekey_instruction,
    is_assign_instruction,
    is_select_instruction,
    is_path_syntax
)

type InstructionChecker = Callable[[str], bool]
type InstructionChecker = Callable[[RawInstruction], AnalyzedInstruction]
type ParsersList = list[tuple[InstructionChecker, InstructionParser]]

class InstructionAnalyzer:
    _PARSERS: ParsersList = [
        (is_delete_instruction, parse_delete_instruction),
        (is_rekey_instruction, parse_rekey_instruction),
        (is_assign_instruction, parse_assign_instruction),
        (is_select_instruction, parse_select_instruction)
    ]
    
    def analyze(self, raw_instruction: RawInstruction) -> AnalyzedInstruction:
        normalized: str = raw_instruction.normalized()
        
        if not normalized:
            raise ValueError("Empty instruction")
        
        for checker, parser in self._PARSERS:
            if checker(normalized):
                return parser(raw_instruction)
        
        if is_path_syntax(normalized):
            return parse_select_instruction(raw_instruction)
            
        raise ValueError(f"Invalid instruction: '{normalized}'")