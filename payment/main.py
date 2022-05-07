
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests, time
from model import Order
from fastapi.background import BackgroundTasks
from database import redis

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/api/orders/{pk}")
def get(pk:str):
    order = Order.get(pk)
    return order


@app.post("/api/orders")
async def create_order(request: Request, background_task: BackgroundTasks):
    body = await request.json()
    # making use of a package "requests" to get the product info from the inventory service
    # and communicating with eact other
    req = requests.get("http://localhost:8000/api/products/%s" % body["id"])
    product = req.json()
    order = Order(
        product_id = body["id"],
        price = product["price"],
        fee = 0.2 * product["price"],
        total = 1.2 * product["price"],
        quantity = body["quantity"],
        status = "pending"
    )
    order.save()
    background_task.add_task(order_completed, order )
    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()
    # sending events from one service to another using redis stream
    # want to reduce the quantity in the inventory service depending on the ordered quantity
    redis.xadd("order_completed", order.dict(), "*")



