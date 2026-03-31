from app.data.database import SessionLocal, init_db
from app.data.models import Classroom, Student
from app.domain.schemas import EvaluationConfig, SimulationConfig
from app.services.analytics import build_final_results
from app.simulation.engine import AcademicSimulator, SimulationContext
from seed_data import run_seed


def test_scenario_results_generation() -> None:
    run_seed()
    init_db()
    db = SessionLocal()

    classroom = db.query(Classroom).filter_by(name="Turma A").first()
    assert classroom is not None
    students = db.query(Student).filter_by(classroom_id=classroom.id).all()

    eval_config = EvaluationConfig(20, 40, 40)
    sim_config = SimulationConfig(total_sprints=10, weeks_per_sprint=2, scenario_name="free_variation")

    simulator = AcademicSimulator(db)
    timeline = simulator.run(SimulationContext(classroom, students, eval_config, sim_config))
    final = build_final_results(timeline)

    assert len(final) == len(students)
    assert {"aprovado", "recuperacao", "reprovado"}.intersection(set(final["final_status"]))

    db.close()
