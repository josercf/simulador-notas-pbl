from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd
import simpy
from sqlalchemy.orm import Session

from app.data.models import Classroom, ScenarioResult, SimulationRun, Student, StudentContribution
from app.domain.schemas import EvaluationConfig, SimulationConfig
from app.services.calculations import (
    calculate_cumulative_grade,
    calculate_cv,
    calculate_individual_artifact_grade,
    classify_student,
    project_final_grade,
)
from app.services.evolution import enforce_target_cv, evolve_factor


@dataclass
class SimulationContext:
    classroom: Classroom
    students: list[Student]
    eval_config: EvaluationConfig
    sim_config: SimulationConfig


class AcademicSimulator:
    def __init__(self, db: Session, seed: int = 42) -> None:
        self.db = db
        self.rng = random.Random(seed)

    def run(self, context: SimulationContext) -> pd.DataFrame:
        env = simpy.Environment()
        run = SimulationRun(scenario_name=context.sim_config.scenario_name)
        self.db.add(run)
        self.db.flush()

        records: list[dict] = []
        state: dict[int, dict[str, float]] = {
            s.id: {"factor": 0.7, "artifact": 0.0, "activity": 0.0, "exam": 20.0} for s in context.students
        }

        def weekly_process() -> simpy.events.Event:
            for sprint in range(1, context.sim_config.total_sprints + 1):
                for _ in range(context.sim_config.weeks_per_sprint):
                    for st in context.students:
                        act = self.rng.uniform(0.4, 1.0) * (
                            context.eval_config.activity_points
                            / (context.sim_config.total_sprints * context.sim_config.weeks_per_sprint)
                        )
                        state[st.id]["activity"] += act
                    yield env.timeout(1)

                group_grade = self.rng.uniform(6.0, 10.0) * (
                    context.eval_config.artifact_points / context.sim_config.total_sprints / 10.0
                )

                factors = []
                for st in context.students:
                    prev_factor = state[st.id]["factor"]
                    new_factor = evolve_factor(st.profile, prev_factor, sprint, self.rng)
                    factors.append(new_factor)
                    state[st.id]["factor"] = new_factor

                if context.sim_config.scenario_name == "cv21_controlled":
                    adjusted = enforce_target_cv(factors, context.sim_config.target_cv)
                    for st, new_factor in zip(context.students, adjusted, strict=True):
                        state[st.id]["factor"] = new_factor

                cv_value = calculate_cv([state[s.id]["factor"] for s in context.students])

                for st in context.students:
                    artifact_grade = calculate_individual_artifact_grade(group_grade, state[st.id]["factor"])
                    state[st.id]["artifact"] += artifact_grade
                    cumulative = calculate_cumulative_grade(
                        state[st.id]["exam"], state[st.id]["artifact"], state[st.id]["activity"]
                    )
                    projected = project_final_grade(cumulative, sprint, context.sim_config.total_sprints)
                    risk = classify_student(projected)

                    records.append(
                        {
                            "run_id": run.id,
                            "scenario": context.sim_config.scenario_name,
                            "student_id": st.id,
                            "student": st.name,
                            "profile": st.profile,
                            "sprint": sprint,
                            "factor": state[st.id]["factor"],
                            "artifact_grade": artifact_grade,
                            "activity_grade": state[st.id]["activity"],
                            "cumulative_grade": cumulative,
                            "projected_final_grade": projected,
                            "risk_level": risk,
                            "cv_factors": cv_value,
                        }
                    )
                    self.db.add(
                        StudentContribution(
                            run_id=run.id,
                            student_id=st.id,
                            sprint_number=sprint,
                            factor=state[st.id]["factor"],
                        )
                    )
                    self.db.add(
                        ScenarioResult(
                            run_id=run.id,
                            student_id=st.id,
                            sprint_number=sprint,
                            artifact_grade=artifact_grade,
                            activity_grade=state[st.id]["activity"],
                            cumulative_grade=cumulative,
                            projected_final_grade=projected,
                            risk_level=risk,
                        )
                    )

            return env.timeout(0)

        env.process(weekly_process())
        env.run()
        self.db.commit()
        return pd.DataFrame.from_records(records)
