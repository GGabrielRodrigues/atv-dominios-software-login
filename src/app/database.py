import sqlite3
from collections.abc import Generator
from pathlib import Path

from app.security import hash_password

DATABASE_PATH = Path(__file__).resolve().parent.parent / "users.db"
DEFAULT_USER_EMAIL = "usuario@teste.com"
DEFAULT_USER_PASSWORD = "teste123"


# Cria o banco de dados na raiz do projeto se ainda não existir
def initialize_database() -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                hashed_password TEXT NOT NULL
            )
            """
        )
        connection.execute(  # Adiciona um dado de usuário fictício no banco
            """
            INSERT OR IGNORE INTO users (email, hashed_password)
            VALUES (?, ?)
            """,
            (DEFAULT_USER_EMAIL, hash_password(DEFAULT_USER_PASSWORD)),
        )


# Cria a conexão com o banco de dados
def get_db() -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()
