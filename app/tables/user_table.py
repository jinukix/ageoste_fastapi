from peewee import *
from app.config import BaseModel


class ShopTable(BaseModel):
    city = CharField(45)
    name = CharField(45)
    address = CharField(1000)
    phone_number = CharField(800)
    work_day = CharField(800)

    class Meta:
        db_Table = "shops"


class MembershipTable(BaseModel):
    grade = CharField(800)
    discount_rate = IntegerField()

    class Meta:
        db_Table = "memberships"


class CouponTable(BaseModel):
    name = CharField()
    discount_rate = IntegerField()
    description = TextField()

    class Meta:
        db_Table = "coupons"


class UserTable(BaseModel):
    name = CharField(max_length=45)
    email = CharField(max_length=400)
    password = CharField(max_length=100)
    phone_number = CharField(max_length=45)
    date_of_birth = DateField()
    address = CharField(max_length=1000)
    is_active = BooleanField(default=True)

    favorite_shop = ForeignKeyField(ShopTable, backref="users")
    membership = ForeignKeyField(MembershipTable, backref="users")
    coupons = ManyToManyField(CouponTable, backref="users")

    class Meta:
        db_table = "users"


class UserCouponsTable(BaseModel):
    user = ForeignKeyField(UserTable)
    coupon = ForeignKeyField(CouponTable)

    class Meta:
        db_Table = "user_coupons"
