from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy import String, Date, DateTime, insert, text
from datetime import datetime

HOST = "200.19.224.150"
USUARIO = "alunos"
SENHA = "AlunoFatec"
BANCO = "atividade2"

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

# Funções de anonimização
def mascarar_primeira_letra(texto):
    """Mantém só a primeira letra e troca o resto por '*'. Ex.: Olivia -> O*****"""
    if not texto:
        return texto
    return texto[0] + "*" * (len(texto) - 1)


def anonimizar_nome(nome):
    """'Olivia Araújo' -> 'O***** Araújo' (só o primeiro nome é mascarado)."""
    partes = nome.split(" ")
    partes[0] = mascarar_primeira_letra(partes[0])
    return " ".join(partes)


def anonimizar_cpf(cpf):
    """'237.615.809-59' -> '237.***.***-**' (mantém os 3 primeiros caracteres e a pontuação)."""
    resto = "".join("*" if c.isdigit() else c for c in cpf[3:])
    return cpf[:3] + resto


def anonimizar_email(email):
    """'nuneserick@example.com' -> 'n*********@example.com' (mascara só antes do @)."""
    if "@" not in email:
        return mascarar_primeira_letra(email)
    usuario, dominio = email.split("@", 1)
    return mascarar_primeira_letra(usuario) + "@" + dominio


def anonimizar_telefone(telefone):
    """'+55 (011) 9483-6810' -> '6810' (só os 4 últimos caracteres)."""
    return telefone[-4:]


def LGPD(row):
    dados = list(row)
    dados[1] = anonimizar_nome(dados[1])
    dados[2] = anonimizar_cpf(dados[2])
    dados[3] = anonimizar_email(dados[3])
    dados[4] = anonimizar_telefone(dados[4])
    return tuple(dados)


if __name__ == "__main__":
    users = []
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios LIMIT 10;"))
        for row in result:
            users.append(LGPD(row))

    for user in users:
        print(user)