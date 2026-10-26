import sqlite3
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import get_db, initialize_database
from app.schemas import LoginRequest, LoginResponse
from app.security import authenticate_user


app = FastAPI(title="Login API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) #Configuração do middleware CORS para permitir solicitações de qualquer origem, com qualquer método e cabeçalho.


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()


@app.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest, #Modelo de dados recebido, email e password
    connection: Annotated[sqlite3.Connection, Depends(get_db)], #Faz com que a função get_db seja chamada automaticamente
) -> LoginResponse:
    authenticated = authenticate_user(
        connection,
        credentials.email,
        credentials.password,
    )
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return LoginResponse(authenticated=True)

app.mount("/", StaticFiles(directory="static", html=True), name="static")