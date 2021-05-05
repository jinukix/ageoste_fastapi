from fastapi import APIRouter, status, Depends

router = APIRouter(tags=["order"], prefix="/order")