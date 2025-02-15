***Payment service***

1) Start app command 
- uvicorn main:app --reload --port=8001


2) u can add simple react app to work with ui

3) postman urls:

1) POST http://127.0.0.1:8001/orders
- create a new order
- parameters: {
    "id": "01JM43T3RKAEBYGQJ25ZCXZRDD",
    "quantity": 2
}
2) GET http://127.0.0.1:8001/orders/01JM43T9W0K23R8HQYMQQZ6RYS/
- get order status