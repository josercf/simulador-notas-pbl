from __future__ import annotations

import random


def bounded(value: float, low: float = 0.05, high: float = 1.0) -> float:
    return max(low, min(high, value))


def evolve_factor(profile: str, prev_factor: float, sprint: int, rng: random.Random) -> float:
    """Atualiza fator individual com base no perfil do aluno."""
    noise = rng.uniform(-0.05, 0.05)

    if profile == "estavel_alto":
        return bounded(0.9 + noise)
    if profile == "estavel_medio":
        return bounded(0.7 + noise)
    if profile == "estavel_baixo":
        return bounded(0.45 + noise)
    if profile == "crescimento_gradual":
        trend = min(0.35, sprint * 0.03)
        return bounded(prev_factor + 0.015 + trend / 10 + noise)
    if profile == "queda_engajamento":
        decay = min(0.35, sprint * 0.03)
        return bounded(prev_factor - 0.02 - decay / 10 + noise)
    if profile == "volatil":
        return bounded(prev_factor + rng.uniform(-0.2, 0.2))

    return bounded(prev_factor + noise)


def enforce_target_cv(factors: list[float], target_cv: float) -> list[float]:
    """Ajusta fatores para aproximar CV alvo mantendo média."""
    if not factors:
        return factors
    mu = sum(factors) / len(factors)
    centered = [f - mu for f in factors]
    current_var = sum(c**2 for c in centered) / len(centered)
    if current_var == 0:
        return [bounded(mu) for _ in factors]
    current_std = current_var**0.5
    desired_std = target_cv * mu
    scale = desired_std / current_std if current_std else 1.0
    adjusted = [bounded(mu + c * scale) for c in centered]
    return adjusted
