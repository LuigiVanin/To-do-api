from pydantic import BaseModel


class UserScheme(BaseModel):
    name: str
    email: str
    age: int
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    age: int

    class Config:
        orm_mode = True
# falta de role em UserScheme

