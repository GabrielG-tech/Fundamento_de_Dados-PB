import pandas as pd
import pathlib

def ler_csv():
    cur_dir = pathlib.Path(__file__).parent.resolve()
    ARQ_ENT = str(cur_dir) + "\\alunos.csv"
    df = pd.read_csv(ARQ_ENT, sep=",", encoding = "utf-8")
    return df

df = ler_csv()

alunos = df[["Nome", "Telefone"]].drop_duplicates().reset_index(drop=True).reset_index() \
            .rename(columns={"index": "id_aluno", "Nome": "nome", "Telefone": "telefone"})
alunos["id_aluno"] += 1
print(alunos)

emails = df[["Nome", "Email"]].drop_duplicates().dropna(axis="index").reset_index(drop=True).reset_index() \
            .rename(columns={"index": "id_email", "Nome": "nome", "Email": "email"})
emails["id_email"] += 1
emails = emails.merge(alunos, how="left", left_on="nome", right_on="nome")
emails = emails[["id_email", "email", "id_aluno"]]
print(emails)

disciplinas = df[["Disciplina"]].drop_duplicates().dropna(axis="index").reset_index(drop=True).reset_index() \
            .rename(columns={"index": "id_disciplina", "Disciplina": "disciplina"})
disciplinas["id_disciplina"] += 1
print(disciplinas)

aluno_disciplina = alunos[["id_aluno", "nome"]].merge(df[["Disciplina", "Nome"]] \
            .drop_duplicates(), left_on="nome", right_on="Nome").dropna()
#print(aluno_disciplina)
aluno_disciplina = aluno_disciplina.merge(disciplinas, how="left", left_on="Disciplina", right_on="disciplina")
#print(aluno_disciplina)
aluno_disciplina = aluno_disciplina[["id_aluno", "id_disciplina"]]
print(aluno_disciplina)