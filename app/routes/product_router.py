from typing import Optional, List

from peewee import *
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from playhouse.shortcuts import model_to_dict

from app.schemas.request.user_request import AuthorizedUser
from app.schemas.request.product_request import ReviewRequestInfo
from app.schemas.response.product_response import ReviewResponseInfo, ReplyResponseInfo, \
    RepliesResponseInfo, ProductResponseInfo, ProductsResponseInfo, ImageInfo
from app.tables.product_table import ProductTable, ReviewTable, ImageTable, ReplyTable, ProductColorImageTable, \
    ColorTable
from app.tables.user_table import UserTable
from app.token import get_current_user


router = APIRouter(tags=["product"], prefix="/product")


@router.get("/", status_code=status.HTTP_200_OK, response_model=ProductsResponseInfo)
def get_products(
        offset: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        colors: Optional[List[str]] = None,
        sizes: Optional[List[str]] = None,
        order_by: Optional[str] = 'id',
        search_by: Optional[str] = None,
):

    filter_set = {}

    if category:
        filter_set['category__name'] = category

    if colors:
        filter_set["productcolorimages__color__name__in"] = colors

    if search_by:
        filter_set['name__icontains'] = search_by

    if sizes:
        filter_set['sizes__name__in'] = sizes

    if order_by == 'name':
        order_by = ProductTable.name
    elif order_by == '-name':
        order_by = ProductTable.name.desc()
    elif order_by == 'id':
        order_by = ProductTable.id
    elif order_by == '-id':
        order_by = ProductTable.id.desc()
    elif order_by == 'price':
        order_by = ProductTable.price
    elif order_by == '-price':
        order_by = ProductTable.price.desc()

    products = ProductTable.select().filter(**filter_set).order_by(order_by)

    products_response = []
    for product in products.prefetch(ProductColorImageTable, ImageTable, ColorTable, ReviewTable)[offset:limit]:
        product.price = int(product.price)

        result = ReviewTable\
            .select(fn.AVG(ReviewTable.score).alias("reviews_score_avg"))\
            .where(ReviewTable.product == product).group_by(ReviewTable.score)

        product.reviews_score_avg = result[0].reviews_score_avg if result else 0

        result = ProductColorImageTable.select(ProductColorImageTable).where(ProductColorImageTable.product == product).first()
        product.thumbnail = ImageInfo(url=result.image.url)

        result = ProductTable \
            .select(fn.COUNT(ProductColorImageTable.color.distinct()).alias("color_count")) \
            .join(ProductColorImageTable) \
            .where(ProductColorImageTable.product == product) \
            .group_by(ProductColorImageTable.color).first()

        product.color_count = result.color_count
        products_response.append(ProductResponseInfo.from_orm(product))

    return ProductsResponseInfo(
        products_count=products.count(),
        products=products_response
    )


@router.post("/{product_id}/review/", status_code=status.HTTP_201_CREATED)
def create_review(req: ReviewRequestInfo, product_id: int, authorized: AuthorizedUser = Depends(get_current_user)):
    try:
        user = UserTable.get(id=authorized.user_id)
        product = ProductTable.get(id=product_id)
        image = ImageTable.create(url=req.image_url)

        ReviewTable.create(
            score=req.score,
            description=req.description,
            image=image,
            user=user,
            product=product,
        )

        return "created review"

    except UserTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists User")
    except ProductTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Product")


@router.put("/{product_id}/review/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewResponseInfo)
def update_review(
        req: ReviewRequestInfo,
        product_id: int,
        review_id: int,
        authorized: AuthorizedUser = Depends(get_current_user)
):
    try:
        product = ProductTable.get(id=product_id)
        review = ReviewTable.get(id=review_id)

        if review.product != product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 상품의 리뷰가 아닙니다!")

        if not req.image_url:
            image = ImageTable.create(url=req.image_url)
            review.image = image

        return ReviewResponseInfo(
            id=review.id,
            score=review.score,
            description=review.description,
            image_url=review.image.url,
            product_name=review.product.name,
            user_email=review.user.email
        )

    except ReviewTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Review")
    except ProductTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Product")


@router.delete("/{product_id}/review/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
        product_id: int,
        review_id: int,
        authorized: AuthorizedUser = Depends(get_current_user)
):
    try:
        product = ProductTable.get(id=product_id)
        review = ReviewTable.get(id=review_id)

        if review.product != product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 상품의 리뷰가 아닙니다!")

        review.delete()
        return "deleted review"

    except ReviewTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Review")
    except ProductTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Product")


@router.get("/{product_id}/review/{review_id}/reply", status_code=status.HTTP_200_OK)
def get_replies(
        product_id: int,
        review_id: int,
        authorized: AuthorizedUser = Depends(get_current_user)
):
    try:
        product = ProductTable.get(id=product_id)
        review = ReviewTable.get(id=review_id)

        if review.product != product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 상품의 리뷰가 아닙니다!")

        replies = ReplyTable.select().where(ReplyTable.review == review)
        replies_response = []

        for reply in replies:
            reply.user_email = reply.user.email
            replies_response.append(ReplyResponseInfo.from_orm(reply))

        return RepliesResponseInfo(
            replies=replies_response
        )

    except ReviewTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Review")
    except ProductTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Product")


@router.post("/{product_id}/review/{review_id}/reply", status_code=status.HTTP_200_OK)
def create_reply(
        product_id: int,
        review_id: int,
        comment: Optional[str] = None,
        authorized: AuthorizedUser = Depends(get_current_user)
):
    try:
        user = UserTable.get(id=authorized.user_id)
        product = ProductTable.get(id=product_id)
        review = ReviewTable.get(id=review_id)

        if review.product != product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 상품의 리뷰가 아닙니다!")

        ReplyTable.create(
            comment=comment,
            user=user,
            review=review
        )

        return "Created reply!"

    except UserTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists User")
    except ReviewTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Review")
    except ProductTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Product")


@router.put("/{product_id}/review/{review_id}/reply/{reply_id}", status_code=status.HTTP_200_OK)
def update_reply(
        product_id: int,
        review_id: int,
        reply_id: int,
        comment: Optional[str] = None,
        authorized: AuthorizedUser = Depends(get_current_user)
):
    try:
        product = ProductTable.get(id=product_id)
        review = ReviewTable.get(id=review_id)
        reply = ReplyTable.get(id=reply_id)

        if review.product != product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 상품의 리뷰가 아닙니다!")

        if reply.review != review:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 리뷰의 댓글이 아닙니다!")

        reply.comment = comment
        reply.save()

        return "Updated reply!"

    except ReplyTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Reply")
    except ReviewTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Review")
    except ProductTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Product")


@router.put("/{product_id}/review/{review_id}/reply/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reply(
        product_id: int,
        review_id: int,
        reply_id: int,
        comment: Optional[str] = None,
        authorized: AuthorizedUser = Depends(get_current_user)
):
    try:
        product = ProductTable.get(id=product_id)
        review = ReviewTable.get(id=review_id)
        reply = ReplyTable.get(id=reply_id)

        if review.product != product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 상품의 리뷰가 아닙니다!")

        if reply.review != review:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="해당 리뷰의 댓글이 아닙니다!")

        reply.delete()

        return "Deleted reply!"

    except ReplyTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Reply")
    except ReviewTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Review")
    except ProductTable.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does Not Exists Product")