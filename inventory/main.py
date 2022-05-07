from fastapi import FastAPI, HTTPException
from model import Product
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/api/products")
def all_products():
    return [format(product_details) for product_details in Product.all_pks()]


def format(product_details:str):
    product = Product.get(product_details)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


@app.post("/api/products/create")
def create_product(product: Product):
    new_product = product.save()
    if new_product:
        return new_product
    raise HTTPException(404, f"Error occur while creating a new product")


@app.get("/api/products/{pk}")
def get_single_product(pk:str):
    product = Product.get(pk)
    if product:
        return product
    raise HTTPException(500, f"There is no product with {pk}")


@app.delete("/api/products/delete/{pk}")
def delete_product(pk:str):
    product = Product.delete(pk)
    if product:
        return product
    raise HTTPException(404, f"There is no product with {pk}")

