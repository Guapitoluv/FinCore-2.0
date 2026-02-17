from pathlib import Path
from typing import Any
import json

from fincore.application.ports.persistence_handler import PersistenceHandler


class JsonHandler(PersistenceHandler):
    def __init__(self, path: Path) -> None:
        self.path: Path = path
    
    
    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            raise FileNotFoundError(self.path)
        
        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)
    
    
    def save(self, data: dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )