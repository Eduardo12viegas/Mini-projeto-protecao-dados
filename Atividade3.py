import csv
import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy import String, Date, DateTime, insert, text
from datetime import datetime

HOST = "200.19.224.150"
USUARIO = "alunos"
SENHA = "AlunoFatec"
BANCO = "atividade2"

# Configurações do arquivo gerado
PASTA_SAIDA = "saida"
SEPARADOR = ";" 

engine = create_engine(f"postgresql+psycopg2://{USUARIO}:{SENHA}@{HOST}:5432/{BANCO}")
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

# Atividade 3: um único arquivo com todos os registros

def gerar_arquivo_todos():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Busca só as duas colunas pedidas, de todos os registros
    with engine.connect() as conn:
        result = conn.execute(text("SELECT nome, cpf FROM usuarios;"))
        registros = [tuple(row) for row in result]

    caminho = os.path.join(PASTA_SAIDA, "todos.csv")
    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=SEPARADOR)
        escritor.writerow(["nome", "cpf"])
        escritor.writerows(registros)
    print(f"{caminho}: {len(registros)} registro(s)")


if __name__ == "__main__":
    gerar_arquivo_todos()
