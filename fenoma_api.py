from fastapi import FastAPI, HTTPException
from typing import List
import requests
from fastapi_redis_cache import FastApiRedisCache, cache
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Declarar los atributos necesarios con tipos
class Data(BaseModel):
    orders: List[dict]
    criterion: str

redis_cache = FastApiRedisCache()
redis_cache.init(host_url="redis://localhost:6379", prefix="fenoma_api-cache")

app = FastAPI(title="Fenoma API")

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/fenoma/1")
async def root():
    return {"message": "Endpoint  #1"}

@app.post("/solution")
# @cache()
async def solution_endpoint(data: Data):
    result = process_orders(data.orders, data.criterion)
    return result
def process_orders(orders, criterion):
    filtered_orders = []
    for order in orders:
        #  Validar parametros de entrada
        if order["price"] < 0 or order["id"] <= 0 or order["quantity"] <= 0:
            raise HTTPException(status_code=422, detail="Data cannot be negative")
        if type(order["status"]) != str or type(order["item"]) != str:
            raise HTTPException(status_code=422, detail="Data must be string")
        # Agregar pedido a lista de pedidos filtrados
        elif order["status"] == criterion and order["price"] >= 0:
            filtered_orders.append(order)
    total_revenue = sum([order["quantity"] * order["price"] for order in filtered_orders])
    return total_revenue

