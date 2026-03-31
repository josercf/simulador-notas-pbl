from __future__ import annotations

import random

from app.data.database import SessionLocal, init_db
from app.data.models import (
    AssessmentItem,
    Classroom,
    Course,
    Group,
    Module,
    Sprint,
    Student,
    Week,
)

PROFILES = [
    "estavel_alto",
    "estavel_medio",
    "estavel_baixo",
    "crescimento_gradual",
    "queda_engajamento",
    "volatil",
]


def run_seed() -> None:
    init_db()
    rng = random.Random(7)
    db = SessionLocal()

    db.query(Week).delete()
    db.query(Sprint).delete()
    db.query(Student).delete()
    db.query(Group).delete()
    db.query(AssessmentItem).delete()
    db.query(Classroom).delete()
    db.query(Module).delete()
    db.query(Course).delete()
    db.commit()

    course = Course(name="Engenharia de Software")
    module = Module(name="PBL 2026.1", course=course)
    classroom = Classroom(name="Turma A", module=module, total_sprints=10, weeks_per_sprint=2)
    db.add_all([course, module, classroom])
    db.flush()

    groups = [Group(name=f"Grupo {i+1}", classroom=classroom) for i in range(5)]
    db.add_all(groups)
    db.flush()

    for i in range(30):
        student = Student(
            name=f"Aluno {i+1:02d}",
            profile=PROFILES[i % len(PROFILES)],
            classroom=classroom,
            group=groups[i % 5],
        )
        db.add(student)

    for sprint in range(1, 11):
        db.add(Sprint(classroom_id=classroom.id, sprint_number=sprint))
        for wk in range(1, 3):
            global_week = (sprint - 1) * 2 + wk
            db.add(Week(classroom_id=classroom.id, sprint_number=sprint, week_number=global_week))

    db.add_all(
        [
            AssessmentItem(classroom_id=classroom.id, item_type="exam", name="Prova final", max_points=20, weight=0.2),
            AssessmentItem(
                classroom_id=classroom.id,
                item_type="artifact",
                name="Artefatos de sprint",
                max_points=40,
                weight=0.4,
            ),
            AssessmentItem(
                classroom_id=classroom.id,
                item_type="activity",
                name="Atividades ponderadas",
                max_points=40,
                weight=0.4,
            ),
        ]
    )

    db.commit()
    db.close()
    print("Seed concluída com sucesso.")


if __name__ == "__main__":
    run_seed()
