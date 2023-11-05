from typing import List
from fastapi import FastAPI
from first_app.models.models import Product

app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


@app.get("/product/{product_id}")
async def read_product(product_id: int):
    for product in sample_products:
        if product_id == product["product_id"]:
            return product
    return {"message": "Product not found"}


@app.get("/products/search", response_model=List[Product])
async def search_product(keyword: str, category: str = None, limit: int = 10):
    """
    Ещё вариант решения, но он менее читаемый
    searching_products = [product for product in sample_products
                          if keyword.lower() in product["name"].lower() and
                          (category is None or category.lower() in product["category"].lower())]
    return searching_products
    """

    searching_products = []
    for product in sample_products:
        if (keyword.lower() in product["name"].lower() and
                (category is None or category.lower() in product["category"].lower())):
            searching_products.append(product)
    return searching_products[:limit]
