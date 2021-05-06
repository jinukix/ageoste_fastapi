from peewee import *

from app.config import BaseModel, TimeStampModel
from app.tables.user_table import UserTable


class MenuTable(BaseModel):
    name = CharField(max_length=45)

    class Meta:
        db_table = 'menus'


class CategoryTable(BaseModel):
    name = CharField(max_length=45)
    menu = ForeignKeyField(MenuTable, backref='categories')

    class Meta:
        db_table = "categories"


class SizeTable(BaseModel):
    name = CharField(max_length=45)

    class Meta:
        db_table = 'sizes'


class ColorTable(BaseModel):
    name = CharField(max_length=45)

    class Meta:
        db_table = 'colors'


class ImageTable(BaseModel):
    url = TextField()

    class Meta:
        db_table = 'images'


class ProductTable(TimeStampModel):
    name = CharField(max_length=45)
    category = ForeignKeyField(CategoryTable, backref='categories', on_delete='CASCADE')
    code = CharField(max_length=200)
    price = DecimalField(max_digits=20, decimal_places=2)
    description = TextField(null=True)
    discount_rate = IntegerField(default=0)

    sizes = ManyToManyField(SizeTable, backref="products")
    colors = ManyToManyField(ColorTable, backref="products")

    class Meta:
        db_table = "products"


class ProductSizeTable(BaseModel):
    product = ForeignKeyField(ProductTable, on_delete='CASCADE')
    size = ForeignKeyField(SizeTable, on_delete='CASCADE')

    class Meta:
        db_table = "product_sizes"


class ProductColorImageTable(BaseModel):
    product = ForeignKeyField(ProductTable, backref='product_color_images', on_delete='CASCADE')
    color = ForeignKeyField(ColorTable, on_delete='CASCADE')
    image = ForeignKeyField(ImageTable, on_delete='CASCADE')

    class Meta:
        db_table = "product_color_images"


class ReviewTable(TimeStampModel):
    score = IntegerField(default=0)
    description = TextField(null=True)

    user = ForeignKeyField(UserTable, backref='reviews' ,on_delete='CASCADE')
    product = ForeignKeyField(ProductTable, backref='reviews' ,on_delete='CASCADE')
    image = ForeignKeyField(ImageTable, null=True, backref='reviews', on_delete='CASCADE')

    class Meta:
        db_table = 'reviews'


class ReplyTable(TimeStampModel):
    comment = CharField(max_length=1000)

    user = ForeignKeyField(UserTable, backref='replies', on_delete='CASCADE')
    review = ForeignKeyField(ReviewTable, backref='replies', on_delete='CASCADE')

    class Meta:
        db_table = 'replies'
