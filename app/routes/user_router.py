import bcrypt
from datetime import datetime, timedelta
from jose import jwt

from peewee import *
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from app.schemas.request.user_request import SignUpUserRequestInfo, AuthorizedUser
from app.schemas.response.user_response import SignUpUserResponseInfo
from app.tables.user_table import UserTable, CouponTable, UserCouponsTable, MembershipTable
from app.token import get_current_user
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(tags=["user"], prefix="/user")


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpUserResponseInfo)
def signup(req: SignUpUserRequestInfo, current_user: AuthorizedUser = Depends(get_current_user)):
    signup_coupon, _ = CouponTable.get_or_create(
        name="회원가입 쿠폰",
        discount_rate=30,
        description="회원가입 쿠폰입니다."
    )

    membership_bronze, _ = MembershipTable.get_or_create(
        grade="bronze",
        discount_rate=3
    )

    hashed_password = bcrypt.hashpw(req.password.encode("utf-8"), bcrypt.gensalt()).decode()

    if UserTable.select().where(UserTable.email == req.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Exists Email")

    if req.phone_number and UserTable.select().where(UserTable.phone_number == req.phone_number):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Exists Phone_number")

    new_user = UserTable.create(
        email=req.email,
        password=hashed_password,
        name=req.name,
        phone_number=req.phone_number,
        date_of_birth=req.date_of_birth,
        address=req.address,
        membership=membership_bronze
    )

    UserCouponsTable.create(
        user=new_user,
        coupon=signup_coupon
    )

    new_user.save()
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
def login(req: OAuth2PasswordRequestForm = Depends()):
    try:
        user = UserTable.get(email=req.username)

        if not bcrypt.checkpw(req.password.encode("utf-8"), user.password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"user_id": user.id, "exp": expire}
        access_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": access_token, "token_type": "bearer"}
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")