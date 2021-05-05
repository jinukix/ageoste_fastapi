from typing import List, Optional
from app.config import ResponseModel


class AccessTokenResponseInfo(ResponseModel):
    access_token: str
    token_type: str = "bearer"


class MembershipInfo(ResponseModel):
    grade: str
    discount_rate: int


class ShopInfo(ResponseModel):
    city: str
    name: str
    address: str
    phone_number: str
    work_day: str


class AccountResponseInfo(ResponseModel):
    id: int
    email: str
    name: str
    phone_number: str
    date_of_birth: str
    address: str
    membership: MembershipInfo
    favorite_shop: Optional[ShopInfo] = None


class CouponResponseInfo(ResponseModel):
    id: int
    name: Optional[str] = None
    discount_rate: Optional[int] = None
    description: Optional[str] = None


class CouponsResponseInfo(ResponseModel):
    coupons: List[CouponResponseInfo]

