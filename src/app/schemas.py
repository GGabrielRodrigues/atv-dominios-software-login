from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    authenticated: bool


class UserInDB(BaseModel):
    email: str
    hashed_password: str
