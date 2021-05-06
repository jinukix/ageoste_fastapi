from typing import List, Optional
from pydantic import BaseModel


class ReviewRequestInfo(BaseModel):
    score: Optional[int] = 0
    description: Optional[str] = None
    image_url: Optional[str] = None
