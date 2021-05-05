from typing import Optional
from pydantic import BaseModel


class SignUpUserRequestInfo(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None


class AuthorizedUser(BaseModel):
    user_id: Optional[int] = None


class ChangeUserRequestInfo(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    shop_id: Optional[int] = None
