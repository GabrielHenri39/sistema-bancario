from sqlmodel import Field, SQLModel, create_engine, Relationship
from enum import Enum
from datetime import date

class Bancos(Enum):
    """Enum para representar os bancos disponíveis."""
    NUBANK = 'Nubank'
    SANTANDER = 'Santander'
    INTER = 'Inter'
    NEON = 'Neon'
    ITAU = 'Itaú'  

class Status(Enum):
    """Enum para representar o status de uma conta."""
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'

class Conta(SQLModel, table=True):
    """Modelo de uma conta bancária."""
    id: int = Field(primary_key=True)
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)
    valor: float

class Tipos(Enum):
    """Enum para representar os tipos de transações."""
    ENTRADA = 'Entrada'
    SAIDA = 'Saída'

class Historico(SQLModel, table=True):
    """Modelo para armazenar o histórico de movimentações de uma conta."""
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship()
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data: date



sqlite_file_name = "database.db"  
sqlite_url = f"sqlite:///{sqlite_file_name}"  

engine = create_engine(sqlite_url, echo=False)  

def create_db_and_tables():  
    """Cria o banco de dados e as tabelas se ainda não existirem."""
    SQLModel.metadata.create_all(engine)  

if __name__ == "__main__":  
    create_db_and_tables()
