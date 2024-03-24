from pydantic import BaseModel


class User(BaseModel):
    full_name: str
    prodi: str
    fakultas: str
    nim: str
    username: str
    password: str
    email: str
    role: str = "user"


class Login(BaseModel):
    username: str
    password: str
