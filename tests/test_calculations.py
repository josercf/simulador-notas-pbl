from app.services.calculations import calculate_cv, calculate_individual_artifact_grade, classify_student


def test_artifact_grade_rule() -> None:
    assert calculate_individual_artifact_grade(8.0, 1.0) == 8.0
    assert calculate_individual_artifact_grade(8.0, 0.5) == 4.0


def test_cv_calculation() -> None:
    values = [0.5, 1.0, 1.5]
    cv = calculate_cv(values)
    assert round(cv, 4) == 0.4082


def test_classification_rule() -> None:
    assert classify_student(85) == "aprovado"
    assert classify_student(55) == "recuperacao"
    assert classify_student(40) == "reprovado"
