from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")


def plot_mean_grade_by_sprint(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    data = df.groupby(["scenario", "sprint"], as_index=False)["cumulative_grade"].mean()
    sns.lineplot(data=data, x="sprint", y="cumulative_grade", hue="scenario", marker="o", ax=ax)
    ax.set_title("Evolução da nota média por sprint")
    return fig


def plot_final_distribution(final_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data=final_df, x="projected_final_grade", hue="scenario", bins=15, kde=True, ax=ax)
    ax.set_title("Distribuição da nota final")
    return fig


def plot_factor_boxplot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df, x="sprint", y="factor", hue="scenario", ax=ax)
    ax.set_title("Fator individual por sprint")
    return fig


def plot_risk_heatmap(df: pd.DataFrame, scenario: str):
    fig, ax = plt.subplots(figsize=(12, 6))
    scenario_df = df[df["scenario"] == scenario].copy()
    risk_map = {"aprovado": 0, "recuperacao": 1, "reprovado": 2}
    pivot = scenario_df.pivot_table(index="student", columns="sprint", values="risk_level", aggfunc="first")
    numeric = pivot.replace(risk_map)
    sns.heatmap(numeric, cmap="RdYlGn_r", cbar=True, ax=ax)
    ax.set_title(f"Risco acadêmico aluno x sprint ({scenario})")
    return fig


def plot_stacked_status(final_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    pivot = final_df.pivot_table(index="scenario", columns="final_status", values="student_id", aggfunc="count", fill_value=0)
    pivot.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title("Aprovados / Recuperação / Reprovados")
    ax.set_ylabel("Quantidade")
    return fig


def plot_scenario_comparison(final_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=final_df, x="scenario", y="projected_final_grade", estimator="mean", errorbar="sd", ax=ax)
    ax.set_title("Comparação entre cenários")
    return fig
