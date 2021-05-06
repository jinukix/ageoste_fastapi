from typing import List
from app.config import ResponseModel


class ReviewResponseInfo(ResponseModel):
    id: int
    score: str
    description: str
    image_url: str
    product_name: str
    user_email: str


class ReplyResponseInfo(ResponseModel):
    id: int
    review_id: int
    user_email: str
    comment: str


class RepliesResponseInfo(ResponseModel):
    replies: List[ReplyResponseInfo]


class ImageInfo(ResponseModel):
    url: str


class ProductResponseInfo(ResponseModel):
    id: int
    name: str
    price: int
    discount_rate: int
    reviews_score_avg: int
    thumbnail: ImageInfo
    color_count: int


class ProductsResponseInfo(ResponseModel):
    products_count: int
    products: List[ProductResponseInfo]
