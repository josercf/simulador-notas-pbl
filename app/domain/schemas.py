from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvaluationConfig:
    exam_points: float = 20.0
    artifact_points: float = 40.0
    activity_points: float = 40.0

    def validate_total(self) -> None:
        total = self.exam_points + self.artifact_points + self.activity_points
        if round(total, 5) != 100.0:
            raise ValueError(f"Total de pontos precisa fechar em 100 e está em {total}.")


@dataclass
class SimulationConfig:
    total_sprints: int = 10
    weeks_per_sprint: int = 2
    scenario_name: str = "free_variation"
    target_cv: float = 0.21
