from datetime import date
from pydantic import BaseModel


class SignUpUserInfo(BaseModel):
    name: str
    email: str
    phone_number: str
    date_of_birth: date
    password: str


class LoginUserInfo(BaseModel):
    email: str
    password: str
