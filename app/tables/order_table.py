from peewee import *

from app.config import TimeStampModel
from app.tables.user_table import UserTable
from app.tables.product_table import ProductTable, SizeTable, ColorTable, ImageTable


class OrderStatusTable(TimeStampModel):
    status = CharField(max_length=45)

    class Meta:
        db_table = 'order_statuses'


class OrderTable(TimeStampModel):
    user = ForeignKeyField(UserTable, backref='orders', on_delete='CASCADE')
    order_status = ForeignKeyField(OrderStatusTable, backref='orders', on_delete='CASCADE')

    class Meta:
        db_table = 'orders'


class CartTable(TimeStampModel):
    quantity = IntegerField(default=0)

    user = ForeignKeyField(UserTable, backref='carts', on_delete='CASCADE')
    product = ForeignKeyField(ProductTable, backref='carts', on_delete='CASCADE')
    size = ForeignKeyField(SizeTable, backref='carts', on_delete='CASCADE')
    color = ForeignKeyField(ColorTable, backref='carts',on_delete='CASCADE')
    order = ForeignKeyField(OrderTable, backref='carts', on_delete='CASCADE')
    thumbnail = ForeignKeyField(ImageTable, backref='carts', on_delete='CASCADE')

    class Meta:
        db_table = 'carts'
