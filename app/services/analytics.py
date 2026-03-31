from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.services.calculations import classify_student


def build_final_results(df: pd.DataFrame) -> pd.DataFrame:
    idx = df.groupby(["scenario", "student_id"])["sprint"].idxmax()
    final_df = df.loc[idx].copy().reset_index(drop=True)
    final_df["final_status"] = final_df["projected_final_grade"].map(classify_student)
    return final_df


def compare_scenarios(all_runs: list[pd.DataFrame]) -> pd.DataFrame:
    joined = pd.concat(all_runs, ignore_index=True)
    return build_final_results(joined)


def export_csv(df: pd.DataFrame, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path
