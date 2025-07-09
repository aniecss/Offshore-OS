from sqlalchemy.orm import sessionmaker
from app.banco import db

SessionLocal = sessionmaker(bind=db)

def sessao():
    # Cria uma sessão com o banco, entrega ela pra quem chamou (via yield)
    # e garante que ela será fechada depois, evitando conexão pendurada.
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close() # indepente se try de certo ou errado, ele fecha a sessão