import sqlite3

import bcrypt

from app.schemas import UserInDB


def hash_password(password: str) -> str:
    # Cria o Salt e transforma tanto ele quanto a senha em UTF8 para a geração do hash
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# Busca o usuário no banco de dados e retorna None no caso de não ter cadastro
def get_user(connection: sqlite3.Connection, email: str) -> UserInDB | None:
    row = connection.execute(
        """
        SELECT email, hashed_password
        FROM users
        WHERE email = ?
        """,
        (email,),
    ).fetchone()
    if row is None:
        return None

    return UserInDB(email=row["email"], hashed_password=row["hashed_password"])


# Retorna True se usuário existir e a senha estiver correta
def authenticate_user(
    connection: sqlite3.Connection, email: str, password: str
) -> bool:
    user = get_user(connection, email)
    if user is None:
        return False
    return verify_password(password, user.hashed_password)
