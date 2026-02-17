from dataclasses import dataclass

@dataclass(frozen=True)
class RawInstruction:
    """
    Represents a raw DSL instruction as an immutable Value Object.

    Invariants:
    - ...
    - ...
    - ...

    Non-responsibilities:
    - ...
    """
    
    value: str

    def normalized(self) -> str:
        return self.value.strip()
    
    
    def removesuffix(self, suffix: str, normalize=False) -> str:
        normalized: str = self.normalized()
        
        if not normalized.endswith(suffix):
            return normalized if normalize else self
        
        if normalize:
            return normalized
        
        return RawInstruction(normalized.removesuffix(suffix))
    
    
    def split_once(self, sep: str) -> tuple[str, str]:
        return self.normalized().split(sep, 1)
    
    
    def ends_with(self, suffix: str) -> bool:
        return self.normalized().endswith(suffix)
    
    
    def contains(self, token: str) -> bool:
        return token in self.normalized()
    
    
    def is_exit(self) -> bool:
        return self.normalized() in {"exit", "quit", "back", "cancel"}