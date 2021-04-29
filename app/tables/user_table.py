from peewee import *

from app.config import BaseModel, TimeStampModel


class ShopTable(BaseModel):
    city = CharField(45, null=True)
    name = CharField(45, null=True)
    address = CharField(1000, null=True)
    phone_number = CharField(800, null=True)
    work_day = CharField(800, null=True)

    class Meta:
        db_table = "shops"


class MembershipTable(BaseModel):
    grade = CharField(800)
    discount_rate = IntegerField()

    class Meta:
        db_table = "memberships"


class CouponTable(BaseModel):
    name = CharField()
    discount_rate = IntegerField()
    description = TextField(null=True)

    class Meta:
        db_table = "coupons"


class UserTable(TimeStampModel):
    email = CharField(unique=True, max_length=400)
    password = CharField(max_length=100)
    name = CharField(max_length=45)
    phone_number = CharField(unique=True, null=True, max_length=45)
    date_of_birth = DateField(null=True)
    address = CharField(null=True, max_length=1000)
    is_deleted = BooleanField(default=False)

    favorite_shop = ForeignKeyField(ShopTable, null=True, backref="users")
    membership = ForeignKeyField(MembershipTable, backref="users")
    coupons = ManyToManyField(CouponTable, backref="users")

    class Meta:
        db_table = "users"


class UserCouponsTable(BaseModel):
    user = ForeignKeyField(UserTable, null=True)
    coupon = ForeignKeyField(CouponTable, null=True)

    class Meta:
        db_table = "user_coupons"
