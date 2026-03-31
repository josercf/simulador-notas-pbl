# Simulador Acadêmico PBL (MVP)

MVP em **Python 3.11+** para simulação de desempenho estudantil com **eventos discretos (SimPy)**, persistência em **SQLite/SQLAlchemy**, análise com **Pandas** e visualização em **Matplotlib/Seaborn**, com interface mínima em **Streamlit**.

## Funcionalidades implementadas
- Cadastro de turma/alunos/grupos via seed e leitura na UI.
- Matriz avaliativa configurável (prova, artefatos, atividades) com validação de total = 100.
- Linha do tempo com 10 sprints e 2 semanas por sprint (parametrizável).
- Evolução do fator individual por perfil:
  - `estavel_alto`, `estavel_medio`, `estavel_baixo`, `crescimento_gradual`, `queda_engajamento`, `volatil`.
- Dois cenários obrigatórios:
  - `free_variation`
  - `cv21_controlled` (ajuste para perseguir CV ~ 21%)
- Cálculos:
  - nota individual de artefato
  - nota acumulada
  - projeção de nota final
  - coeficiente de variação
  - classificação (aprovado / recuperacao / reprovado)
- Exportação CSV.
- Gráficos analíticos obrigatórios.

## Estrutura do projeto

```text
simulador-notas-pbl/
├── app/
│   ├── api_or_ui/
│   │   └── streamlit_app.py
│   ├── data/
│   │   ├── database.py
│   │   └── models.py
│   ├── domain/
│   │   └── schemas.py
│   ├── services/
│   │   ├── analytics.py
│   │   ├── calculations.py
│   │   └── evolution.py
│   ├── simulation/
│   │   └── engine.py
│   └── visualization/
│       └── plots.py
├── docs/
│   └── example_output.md
├── examples/
├── tests/
│   ├── test_calculations.py
│   ├── test_evolution.py
│   └── test_simulation.py
├── requirements.txt
└── seed_data.py
```

## Como rodar localmente

1. Criar e ativar ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Popular banco SQLite:
```bash
python seed_data.py
```

4. Rodar testes:
```bash
pytest -q
```

5. Subir interface Streamlit:
```bash
streamlit run app/api_or_ui/streamlit_app.py
```

## Regras de cálculo centrais

### Artefato individual
```text
nota_individual_artefato = nota_grupo_artefato * fator_individual_contribuicao
```

### Classificação final
- `aprovado`: nota >= 70
- `recuperacao`: 50 <= nota < 70
- `reprovado`: nota < 50

## Seed inicial
`seed_data.py` cria:
- 1 turma (`Turma A`)
- 30 alunos
- 5 grupos
- 10 sprints e 20 semanas
- matriz avaliativa (20/40/40)
- perfis variados de evolução

## Exemplos de saída
Após rodar simulação na UI, um CSV é salvo em:
- `examples/resultado_final.csv`

Veja também:
- `docs/example_output.md`

## Limitações atuais do MVP
- Não há autenticação de usuários.
- UI é mínima e focada em configuração/execução.
- Regras de geração de nota de grupo dos artefatos usam distribuição probabilística simples.
- Sem versionamento de matrizes avaliativas por execução.

## Próximos passos recomendados
1. Implementar CRUD completo no Streamlit para Course/Module/Classroom/Group/Student.
2. Adicionar filtros avançados e drill-down por aluno/grupo.
3. Criar execução assíncrona para turmas grandes.
4. Implementar relatório PDF e API REST (FastAPI) para integrações.
5. Adicionar calibração estatística dos perfis com dados reais históricos.
