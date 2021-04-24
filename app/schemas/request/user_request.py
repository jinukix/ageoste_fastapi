from typing import List, Optional
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

