from typing import Protocol

from fincore.application.cli.raw_instruction import RawInstruction
from fincore.application.cli.instruction_dtos import AnalyzedInstruction


class InstructionRouterProtocol:
    def route(self, instruction: AnalyzedInstruction) -> None: ...


class InstructionAnalyzerProtocol(Protocol):
    def analyze(self, raw_instruction: RawInstruction) -> AnalyzedInstruction: ...