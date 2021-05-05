from typing import List, Optional
from pydantic import BaseModel


class ProductsRequestInfo(BaseModel):
    menu_id: Optional[int] = None
    category_id: Optional[int] = None
    color_ids: List[int]
    order_by: Optional[str] = "id"
    search_word: Optional[str] = None


class ReviewRequestInfo(BaseModel):
    score: Optional[int] = 0
    description: Optional[str] = None
    image_url: Optional[str] = None
