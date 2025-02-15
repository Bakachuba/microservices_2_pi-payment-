import time, requests

from redis_om import get_redis_connection, HashModel

from fastapi.background import BackgroundTasks
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# for the second service it should be a different database
redis = get_redis_connection(
    host="redis-11937.crce175.eu-north-1-1.ec2.redns.redis-cloud.com",
    port=11937,
    password="4dPh7ulk0N4vodcI49GhdmiYVqLBM7Nd",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, paid, cancelled

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    order = Order.get(pk)
    # redis.xadd('refund_order', order.dict(), '*')
    return order

@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    req = requests.get("http://localhost:8000/products/%s" % body['id'])
    product = req.json()

    print(product)

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=product['price'] * 1.2,
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    redis.xadd('refund_order', order.dict(), '*')  # Ensure stream is created

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'paid'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
    # * - auto generated id
