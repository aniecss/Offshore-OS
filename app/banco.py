from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
import datetime, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "dados.db")

db = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

Base = declarative_base()

class Usuario(Base):
    __tablename__= "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    cpf = Column("CPF", Integer)
    cargo = Column("cargo", String)
    email = Column("email", String)
    senha = Column("senha", String)

    def __init__(self, nome, cpf, cargo, email, senha):
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        self.email = email
        self.senha = senha

class Unidade(Base):
    __tablename__="unidades"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    tipo = Column("tipo", String)
    localidade = Column("localidade", String)

    def __init__(self, nome, tipo, localidade):
        self.nome = nome
        self.tipo = tipo
        self.localidade = localidade

class Equipamento(Base):
    __tablename__="equipamentos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    codigo_tag = Column("codigo_tag", String)
    descricao = Column("descricao", String)
    unidade_id = Column("unidade_id", Integer, ForeignKey("unidades.id"))

    def __init__(self, nome, codigo_tag, descricao, unidade_id):
        self.nome = nome
        self.codigo_tag = codigo_tag
        self.descricao = descricao
        self.unidade_id = unidade_id

class Servico(Base):
    __tablename__ = "servicos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"))
    descricao = Column("descricao", String)
    data_abertura = Column("data_abertura", DateTime)
    status = Column("status", String)
    unidade_id = Column("unidade", Integer, ForeignKey("unidades.id"))
    equipamento_id = Column("equipamento_id", Integer, ForeignKey("equipamentos.id"))

    def __init__(self, usuario_id, descricao, data_abertura, status, unidade_id, equipamento_id):
        self.usuario_id = usuario_id
        self.descricao = descricao
        self.data_abertura = data_abertura
        self.status = status
        self.unidade_id = unidade_id
        self.equipamento_id = equipamento_id

Base.metadata.create_all(db)
print("Banco de dados criado com sucesso")
