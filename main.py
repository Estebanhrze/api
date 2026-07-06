from fastapi import FastAPI
from models.item import Item
from fastapi import FastAPI, Form
from typing import Annotated
from models.form_data import FormData
from fastapi import FastAPI, Form, Response
from fastapi import FastAPI, Form, Response, HTTPException, status



app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "Qux"}, {"item_name": "Quux"}, {"item_name": "Corge"}, {"item_name": "Grault"}, {"item_name": "Garply"}, {"item_name": "Waldo"}, {"item_name": "Fred"}, {"item_name": "Plugh"}, {"item_name": "Xyzzy"}, {"item_name": "Thud"}]

@app.get("/")
def read_root():
    return {"message": "Hola, Fast API!"}

@app.get("/items/{item_id}")
def read_item(item_id):
   return {"item_id": item_id}


@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10, q: str | None = None):
    results = fake_items_db[skip : skip + limit]
    if q:
        results.append({"item_name": q})
    return results

@app.post("/items/")
def create_item(item: Item):
    item_dict = item.model_dump()

    if item_dict is not None:
        fake_items_db.append(item_dict)

    return item_dict

@app.put("/items/{item_name}")
def update_item(item_name: str, item: Item):
    for i, fake_item in enumerate(fake_items_db):
        if fake_item["item_name"] == item_name:
            fake_items_db[i] = item.model_dump()
            return {"item_name": item_name, **item.model_dump()}
    return {"error": "Item not found"}


#solo hay un parametro
#la q viaja como consulta
@app.put("/items/{item_name}/query")
def update_item_with_query(item_name: str, item: Item, q: str | None = None):
    for i, fake_item in enumerate(fake_items_db):
        if fake_item["item_name"] == item_name:
            fake_items_db[i] = item.model_dump()

            response = {
                "item_name": item_name,
                **item.model_dump()
            }

            if q:
                response.update({"q": q})

            return response

    return {"error": "Item not found"}

@app.post("/items_form/")
def create_item(
    item_name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    price: Annotated[float, Form()],
    tax: Annotated[float, Form()]
):

    # Verificar si el item ya existe
    for fake_item in fake_items_db:
        if fake_item["item_name"] == item_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item already exists."
            )

    # Validar impuesto
    if tax < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tax cannot be negative."
        )

    # Crear el objeto FormData
    form_data = FormData(
        item_name=item_name,
        description=description,
        price=price,
        tax=tax
    )

    # Guardar en la base de datos simulada
    fake_items_db.append({
        "item_name": form_data.item_name
    })

    # Mensaje de éxito
    message = (
        f"Item '{form_data.item_name}' created successfully "
        f"with description '{form_data.description}', "
        f"price {form_data.price}, and tax {form_data.tax}."
    )

    return Response(
        content=message,
        status_code=status.HTTP_201_CREATED
    )