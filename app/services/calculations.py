from __future__ import annotations

import math
from statistics import mean


def calculate_individual_artifact_grade(group_grade: float, contribution_factor: float) -> float:
    """Calcula nota individual de artefato com base na nota de grupo e fator individual."""
    return round(group_grade * max(0.0, min(1.0, contribution_factor)), 4)


def calculate_cv(values: list[float]) -> float:
    """Calcula coeficiente de variação (desvio padrão / média)."""
    if not values:
        return 0.0
    mu = mean(values)
    if mu == 0:
        return 0.0
    variance = sum((v - mu) ** 2 for v in values) / len(values)
    std_dev = math.sqrt(variance)
    return std_dev / mu


def calculate_cumulative_grade(
    exam_grade: float,
    artifact_accumulated: float,
    activity_accumulated: float,
) -> float:
    return round(exam_grade + artifact_accumulated + activity_accumulated, 4)


def project_final_grade(current_cumulative: float, current_sprint: int, total_sprints: int) -> float:
    if current_sprint <= 0:
        return 0.0
    projection = current_cumulative * (total_sprints / current_sprint)
    return round(min(100.0, projection), 4)


def classify_student(final_grade: float) -> str:
    if final_grade >= 70:
        return "aprovado"
    if final_grade >= 50:
        return "recuperacao"
    return "reprovado"
