from typing import List, Optional
from app.config import ResponseModel


class ProductListResponseInfo(ResponseModel):
    pass


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