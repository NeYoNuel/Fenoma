from fastapi import FastAPI
from typing import List
import requests

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/fenoma/1")
async def root():
    return {"message": "Endpoint  #1"}

@app.post("/prueba")
async def solution_endpoint(name: str, apellido: str):
    return f"el nombre es {name} y el apellido es {apellido}"

@app.post("/solution")
async def solution_endpoint(orders: List[dict], criterion: str):
    result = process_orders(orders, criterion)
    return result
def process_orders(orders, criterion):
    filtered_orders = [order for order in orders if order["status"] == criterion and order["price"] > 0]
    total_revenue = sum([order["quantity"] * order["price"] for order in filtered_orders])
    return total_revenue


