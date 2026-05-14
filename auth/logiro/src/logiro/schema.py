from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LogConfig:
    level: int = 20  # INFO
    json_enabled: bool = False
