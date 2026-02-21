from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./banco.db"

# Cria o engine (motor) do banco de dados
# connect_args={"check_same_thread": False} é necessário apenas para o SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para a criação dos modelos
Base = declarative_base()

# Dependência para obter a sessão do banco em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
