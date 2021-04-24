# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class CouponTable(peewee.Model):
    name = CharField(max_length=255)
    discount_rate = IntegerField()
    description = TextField()
    class Meta:
        table_name = "coupons"


@snapshot.append
class MembershipTable(peewee.Model):
    grade = CharField(max_length=800)
    discount_rate = IntegerField()
    class Meta:
        table_name = "memberships"


@snapshot.append
class ShopTable(peewee.Model):
    city = CharField(max_length=45)
    name = CharField(max_length=45)
    address = CharField(max_length=1000)
    phone_number = CharField(max_length=800)
    work_day = CharField(max_length=800)
    class Meta:
        table_name = "shops"


@snapshot.append
class UserTable(peewee.Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=45)
    email = CharField(max_length=400)
    password = CharField(max_length=100)
    phone_number = CharField(max_length=45)
    date_of_birth = DateField()
    address = CharField(max_length=1000)
    is_active = BooleanField(default=True)
    favorite_shop = snapshot.ForeignKeyField(backref='users', index=True, model='shoptable')
    membership = snapshot.ForeignKeyField(backref='users', index=True, model='membershiptable')
    class Meta:
        table_name = "users"


@snapshot.append
class UserCouponsTable(peewee.Model):
    user = snapshot.ForeignKeyField(index=True, model='usertable')
    coupon = snapshot.ForeignKeyField(index=True, model='coupontable')
    class Meta:
        table_name = "user_coupons"


