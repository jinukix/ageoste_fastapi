import bcrypt
from jose import jwt

from peewee import *
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from starlette.responses import Response

from app.schemas.request.user_request import SignUpUserRequestInfo, AuthorizedUser, ChangeUserRequestInfo
from app.schemas.response.user_response import AccessTokenResponseInfo, AccountResponseInfo, MembershipInfo, CouponsResponseInfo, CouponResponseInfo
from app.tables.user_table import UserTable, CouponTable, UserCouponsTable, MembershipTable, ShopTable
from app.token import get_current_user
from app.config import SECRET_KEY, ALGORITHM


router = APIRouter(tags=["user"], prefix="/user")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(req: SignUpUserRequestInfo):
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

    return "created user"


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AccessTokenResponseInfo)
def login(req: OAuth2PasswordRequestForm = Depends()):
    try:
        user = UserTable.get(email=req.username)

        if user.is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Is Deleted User")

        if not bcrypt.checkpw(req.password.encode("utf-8"), user.password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

        access_token = jwt.encode({"user_id": user.id}, key=SECRET_KEY, algorithm=ALGORITHM)

        return AccessTokenResponseInfo(access_token=access_token)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")


@router.get("", status_code=status.HTTP_200_OK, response_model=AccountResponseInfo)
def get_account(authorized: AuthorizedUser = Depends(get_current_user)):
    user = UserTable.get(id=authorized.user_id)

    if user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Is Deleted User")

    return AccountResponseInfo(
        id=user.id,
        email=user.email,
        name=user.name,
        phone_number=user.phone_number,
        date_of_birth=user.date_of_birth,
        address=user.address,
        membership=MembershipInfo(
            grade=user.membership.grade,
            discount_rate=user.membership.discount_rate
        ),
        favorite_shop=user.favorite_shop
    )


@router.put("", status_code=status.HTTP_200_OK, response_model=AccountResponseInfo)
def change_account(req: ChangeUserRequestInfo, authorized: AuthorizedUser = Depends(get_current_user)):
    user = UserTable.get(id=authorized.user_id)

    if user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Is Deleted User")

    if req.email:
        if UserTable.select().where(UserTable.email == req.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Exists Email")
        user.email = req.email

    if req.phone_number:
        if UserTable.select().where(UserTable.phone_number == req.phone_number):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Exists Phone number")
        user.phone_number = req.phone_number

    if req.password:
        user.password = bcrypt.hashpw(req.password.encode("utf-8"), bcrypt.gensalt()).decode()

    if req.shop_id:
        user.favorite_shop = ShopTable.get(id=req.shop_id)

    if req.name:
        user.name = req.name

    if req.date_of_birth:
        user.date_of_birth = req.date_of_birth

    if req.address:
        user.address = req.address

    user.save()

    return AccountResponseInfo(
        id=user.id,
        email=user.email,
        name=user.name,
        phone_number=user.phone_number,
        date_of_birth=user.date_of_birth,
        address=user.address,
        membership=MembershipInfo(
            grade=user.membership.grade,
            discount_rate=user.membership.discount_rate
        ),
        favorite_shop=user.favorite_shop
    )


@router.get("/coupon", status_code=status.HTTP_200_OK, response_model=CouponsResponseInfo)
def get_coupons(authorized: AuthorizedUser = Depends(get_current_user)):
    user = UserTable.get(id=authorized.user_id)
    coupons = UserCouponsTable.select().where(UserCouponsTable.user == user)
    coupons_response = [CouponResponseInfo.from_orm(coupon) for coupon in coupons]

    return CouponsResponseInfo(
        coupons=coupons_response
    )
