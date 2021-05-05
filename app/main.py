from fastapi import FastAPI
from app.routes import user_router, product_router, order_router

app = FastAPI()
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
