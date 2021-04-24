from typing import List, Optional
from pydantic import BaseModel


class SignUpUserResponseInfo(BaseModel):
    email: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True
