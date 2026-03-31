from __future__ import annotations

import streamlit as st

from app.data.database import SessionLocal, init_db
from app.data.models import Classroom, Student
from app.domain.schemas import EvaluationConfig, SimulationConfig
from app.services.analytics import build_final_results, compare_scenarios, export_csv
from app.simulation.engine import AcademicSimulator, SimulationContext
from app.visualization.plots import (
    plot_factor_boxplot,
    plot_final_distribution,
    plot_mean_grade_by_sprint,
    plot_risk_heatmap,
    plot_scenario_comparison,
    plot_stacked_status,
)


def run_ui() -> None:
    st.set_page_config(page_title="Simulador Acadêmico PBL", layout="wide")
    st.title("Simulador Acadêmico de Desempenho Estudantil")

    init_db()
    db = SessionLocal()

    st.header("1) Cadastro de turma")
    classroom_name = st.text_input("Nome da turma", value="Turma A")

    classroom = db.query(Classroom).filter_by(name=classroom_name).first()
    if classroom:
        st.success(f"Turma encontrada: {classroom.name}")
    else:
        st.warning("Turma não encontrada. Rode seed_data.py para cadastrar dados iniciais.")
        st.stop()

    students = db.query(Student).filter_by(classroom_id=classroom.id).all()

    st.header("2) Cadastro de alunos e grupos")
    st.write(f"Total de alunos cadastrados: {len(students)}")
    st.dataframe(
        [{"id": s.id, "nome": s.name, "grupo": s.group.name if s.group else None, "perfil": s.profile} for s in students]
    )

    st.header("3) Configuração dos pesos")
    exam_points = st.number_input("Prova fixa", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
    artifact_points = st.number_input("Artefatos", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
    activity_points = st.number_input("Atividades ponderadas", min_value=0.0, max_value=100.0, value=40.0, step=1.0)

    eval_config = EvaluationConfig(exam_points=exam_points, artifact_points=artifact_points, activity_points=activity_points)
    try:
        eval_config.validate_total()
        st.success("Configuração válida (total = 100).")
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    st.header("4) Configuração da simulação")
    total_sprints = st.number_input("Sprints", min_value=1, max_value=20, value=10)
    weeks_per_sprint = st.number_input("Semanas por sprint", min_value=1, max_value=4, value=2)
    target_cv = st.slider("CV alvo (somente cenário cv21_controlled)", min_value=0.05, max_value=0.5, value=0.21)

    if st.button("Rodar Simulação", type="primary"):
        runs = []
        for scenario in ["free_variation", "cv21_controlled"]:
            sim_config = SimulationConfig(
                total_sprints=total_sprints,
                weeks_per_sprint=weeks_per_sprint,
                scenario_name=scenario,
                target_cv=target_cv,
            )
            simulator = AcademicSimulator(db=db, seed=42)
            context = SimulationContext(
                classroom=classroom,
                students=students,
                eval_config=eval_config,
                sim_config=sim_config,
            )
            run_df = simulator.run(context)
            runs.append(run_df)

        all_df = compare_scenarios(runs)
        detailed_df = compare_scenarios([runs[0], runs[1]])
        full_timeline = __import__("pandas").concat(runs, ignore_index=True)
        final_df = build_final_results(full_timeline)

        st.header("5) Resultados")
        st.subheader("Tabela final")
        st.dataframe(final_df)

        csv_path = export_csv(final_df, "examples/resultado_final.csv")
        st.success(f"CSV exportado em {csv_path}")

        st.pyplot(plot_mean_grade_by_sprint(full_timeline))
        st.pyplot(plot_final_distribution(final_df))
        st.pyplot(plot_factor_boxplot(full_timeline))
        st.pyplot(plot_risk_heatmap(full_timeline, scenario="free_variation"))
        st.pyplot(plot_stacked_status(final_df))
        st.pyplot(plot_scenario_comparison(final_df))

        st.subheader("Comparação resumida entre cenários")
        st.dataframe(all_df.groupby("scenario")["projected_final_grade"].agg(["mean", "std", "min", "max"]))
        st.caption(f"Linhas comparadas: {len(detailed_df)}")

    db.close()


if __name__ == "__main__":
    run_ui()
