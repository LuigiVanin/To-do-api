from pydantic import BaseModel


class UserScheme(BaseModel):
    name: str
    email: str
    age: int
    password: str

# falta de role em UserScheme

