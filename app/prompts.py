from dataclasses import dataclass
from typing import Any
import yaml


@dataclass
class PromptConfig:
    greet_template: str
    confirm_template: str
    file_prefix: str




def load_prompts(path: str) -> PromptConfig:
    with open(path, "r", encoding="utf-8") as f:
        data: dict[str, Any] = yaml.safe_load(f) or {}
    return PromptConfig(
        greet_template=data.get("greet_template", "Hola {name}! ¿Tomamos tu pedido?"),
        confirm_template=data.get("confirm_template", "Confirmá por favor: {summary}"),
        file_prefix=data.get("file_prefix", "pedido")
    )