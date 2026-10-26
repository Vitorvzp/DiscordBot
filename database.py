from sqlmodel import SQLModel, Field, create_engine
from time import sleep as s
from runtime_paths import data_file

class IA(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    usuario_id: int
    usuario_nome: str
    mensagem: str
    resposta: str
    data: str


connection_string = f"sqlite:///{data_file('database.db').as_posix()}"

engine = create_engine(connection_string)

SQLModel.metadata.create_all(engine)
