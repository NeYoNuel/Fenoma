import pytest
from fastapi.testclient import TestClient
from fenoma_api import app
client = TestClient(app)
def test_solution_endpoint_input():
    # Datos de prueba
    orders = [  {"id": 1, "item": "Laptop", "quantity": 1, "price": 50.99, "status": "completed"},
                {"id": 2, "item": "Smartphone", "quantity": 2, "price": 30.95, "status": "pending"},
                {"id": 3, "item": "Headphones", "quantity": 3, "price": 15.90, "status": "completed"},
    ]
    criterion = "completed"

    # criterion = "completed"
    # expected_total_revenue = 98.69

    # Realizar la solicitud POST a la API
    response = client.post("/solution", json={"orders": orders, "criterion": criterion})

    # Verificar el código de respuesta
    assert response.status_code == 200

    # Verificar el contenido de la respuesta
    expected_result = 98.69
    assert response.json() == expected_result
def test_solution_endpoint_prices():
    # Datos de prueba con precios válidos y precios no válidos
    orders_valid_prices = [{"id": 2, "item": "Smartphone", "quantity": 2, "price": 30.95, "status": "completed"}]
    orders_invalid_prices = [{"id": 2, "item": "Smartphone", "quantity": 2, "price": -30.95, "status": "completed"}]

    # Realizar la solicitud POST a la API con precios válidos
    response_valid_prices = client.post("/solution", json={"orders": orders_valid_prices, "criterion": "completed"})


    # Verificar que la respuesta para precios válidos sea exitosa
    assert response_valid_prices.status_code == 200

    # Realizar la solicitud POST a la API con precios no válidos
    response_invalid_prices = client.post("/solution", json={"orders": orders_invalid_prices, "criterion": "completed"})

    # Verificar que la respuesta para precios no válidos sea un error
    assert response_invalid_prices.status_code == 422  # 422 Unprocessable Entity
def test_solution_endpoint_result():
    # Datos de prueba
    orders = [{"id": 3, "item": "Headphones", "quantity": 4, "price": 10.00, "status": "completed"}]
    criterion = "completed"

    # Calcular el resultado esperado
    expected_result = 40.00

    # Calcular el resultado real llamando a la función
    real_result = process_orders(orders, criterion)

    # Verificar que el resultado real sea igual al resultado esperado
    assert real_result == expected_result
def process_orders(orders, criterion):
    filtered_orders = []
    for order in orders:
        if order["price"] < 0:
            raise HTTPException(status_code=422, detail="Negative price")
        elif order["status"] == criterion and order["price"] >= 0:
            filtered_orders.append(order)
    total_revenue = sum([order["quantity"] * order["price"] for order in filtered_orders])
    return total_revenue