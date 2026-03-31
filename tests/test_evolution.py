import random

from app.services.calculations import calculate_cv
from app.services.evolution import enforce_target_cv, evolve_factor


def test_evolution_factor_in_bounds() -> None:
    rng = random.Random(10)
    value = evolve_factor("volatil", 0.7, 3, rng)
    assert 0.05 <= value <= 1.0


def test_cv21_controlled_adjustment() -> None:
    factors = [0.4, 0.6, 0.7, 0.9, 0.95]
    adjusted = enforce_target_cv(factors, 0.21)
    cv = calculate_cv(adjusted)
    assert abs(cv - 0.21) < 0.03
