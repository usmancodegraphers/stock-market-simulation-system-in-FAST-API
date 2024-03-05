from fastapi import FastAPI

from routes.user_routes import routes as user
from routes.stockdata_routes import routes as stock
from routes.transactions_routes import routes as transection

app = FastAPI()

app.include_router(user)
app.include_router(stock)
app.include_router(transection)

