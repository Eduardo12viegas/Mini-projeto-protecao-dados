from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy import String, Date, DateTime, insert, text
from datetime import datetime

engine = create_engine("postgresql+psycopg2://user:pass@server:5432/db")
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

def LGPD(row):
    return tuple(row)

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 10;"))
    for row in result:
        users.append(LGPD(row))
