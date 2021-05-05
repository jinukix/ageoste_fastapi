# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class ShopTable(peewee.Model):
    city = CharField(max_length=45, null=True)
    name = CharField(max_length=45, null=True)
    address = CharField(max_length=1000, null=True)
    phone_number = CharField(max_length=800, null=True)
    work_day = CharField(max_length=800, null=True)
    class Meta:
        table_name = "shops"


@snapshot.append
class MembershipTable(peewee.Model):
    grade = CharField(max_length=800)
    discount_rate = IntegerField()
    class Meta:
        table_name = "memberships"


@snapshot.append
class UserTable(peewee.Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    email = CharField(max_length=400, unique=True)
    password = CharField(max_length=100)
    name = CharField(max_length=45)
    phone_number = CharField(max_length=45, null=True, unique=True)
    date_of_birth = DateField(null=True)
    address = CharField(max_length=1000, null=True)
    is_deleted = BooleanField(default=False)
    favorite_shop = snapshot.ForeignKeyField(backref='users', index=True, model='shoptable', null=True)
    membership = snapshot.ForeignKeyField(backref='users', index=True, model='membershiptable')
    class Meta:
        table_name = "users"


@snapshot.append
class MenuTable(peewee.Model):
    name = CharField(max_length=45)
    class Meta:
        table_name = "menus"


@snapshot.append
class CategoryTable(peewee.Model):
    name = CharField(max_length=45)
    menu = snapshot.ForeignKeyField(backref='categories', index=True, model='menutable')
    class Meta:
        table_name = "categories"


@snapshot.append
class ProductTable(peewee.Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=45)
    category = snapshot.ForeignKeyField(backref='categories', index=True, model='categorytable', on_delete='CASCADE')
    code = CharField(max_length=200)
    price = DecimalField(auto_round=False, decimal_places=2, max_digits=20, rounding='ROUND_HALF_EVEN')
    description = TextField(null=True)
    discount_rate = IntegerField(default=0)
    class Meta:
        table_name = "products"


@snapshot.append
class SizeTable(peewee.Model):
    name = CharField(max_length=45)
    class Meta:
        table_name = "sizes"


@snapshot.append
class ColorTable(peewee.Model):
    name = CharField(max_length=45)
    class Meta:
        table_name = "colors"


@snapshot.append
class OrderStatusTable(peewee.Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    status = CharField(max_length=45)
    class Meta:
        table_name = "order_statuses"


@snapshot.append
class OrderTable(peewee.Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    user = snapshot.ForeignKeyField(backref='orders', index=True, model='usertable', on_delete='CASCADE')
    order_status = snapshot.ForeignKeyField(backref='orders', index=True, model='orderstatustable', on_delete='CASCADE')
    class Meta:
        table_name = "orders"


@snapshot.append
class ImageTable(peewee.Model):
    url = TextField()
    class Meta:
        table_name = "images"


@snapshot.append
class CartTable(peewee.Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    quantity = IntegerField(default=0)
    user = snapshot.ForeignKeyField(backref='carts', index=True, model='usertable', on_delete='CASCADE')
    product = snapshot.ForeignKeyField(backref='carts', index=True, model='producttable', on_delete='CASCADE')
    size = snapshot.ForeignKeyField(backref='carts', index=True, model='sizetable', on_delete='CASCADE')
    color = snapshot.ForeignKeyField(backref='carts', index=True, model='colortable', on_delete='CASCADE')
    order = snapshot.ForeignKeyField(backref='carts', index=True, model='ordertable', on_delete='CASCADE')
    thumbnail = snapshot.ForeignKeyField(backref='carts', index=True, model='imagetable', on_delete='CASCADE')
    class Meta:
        table_name = "carts"


@snapshot.append
class CouponTable(peewee.Model):
    name = CharField(max_length=255)
    discount_rate = IntegerField()
    description = TextField(null=True)
    class Meta:
        table_name = "coupons"


@snapshot.append
class ProductColorImageTable(peewee.Model):
    product = snapshot.ForeignKeyField(index=True, model='producttable', on_delete='CASCADE')
    color = snapshot.ForeignKeyField(index=True, model='colortable', on_delete='CASCADE')
    image = snapshot.ForeignKeyField(index=True, model='imagetable', on_delete='CASCADE')
    class Meta:
        table_name = "product_color_images"


@snapshot.append
class ProductSizeTable(peewee.Model):
    product = snapshot.ForeignKeyField(index=True, model='producttable', on_delete='CASCADE')
    size = snapshot.ForeignKeyField(index=True, model='sizetable', on_delete='CASCADE')
    class Meta:
        table_name = "product_sizes"


@snapshot.append
class ReviewTable(peewee.Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    score = IntegerField(default=0)
    description = TextField(null=True)
    user = snapshot.ForeignKeyField(backref='reviews', index=True, model='usertable', on_delete='CASCADE')
    product = snapshot.ForeignKeyField(backref='reviews', index=True, model='producttable', on_delete='CASCADE')
    image = snapshot.ForeignKeyField(backref='reviews', index=True, model='imagetable', null=True, on_delete='CASCADE')
    class Meta:
        table_name = "reviews"


@snapshot.append
class ReplyTable(peewee.Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    comment = CharField(max_length=1000)
    user = snapshot.ForeignKeyField(backref='replies', index=True, model='usertable', on_delete='CASCADE')
    review = snapshot.ForeignKeyField(backref='replies', index=True, model='reviewtable', on_delete='CASCADE')
    class Meta:
        table_name = "replies"


@snapshot.append
class UserCouponsTable(peewee.Model):
    user = snapshot.ForeignKeyField(index=True, model='usertable', null=True)
    coupon = snapshot.ForeignKeyField(index=True, model='coupontable', null=True)
    class Meta:
        table_name = "user_coupons"


def backward(old_orm, new_orm):
    usercouponstable = new_orm['usercouponstable']
    return [
        # Check the field `usercouponstable.coupon` does not contain null values
        # Check the field `usercouponstable.user` does not contain null values
    ]
