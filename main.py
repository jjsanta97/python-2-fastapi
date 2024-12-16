from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Configuración de templates. Jinja2 permite renderizar plantillas
templates = Jinja2Templates(directory="templates")


# Modelos de datos de carros y usuarios con Pydantic
class Car(BaseModel):
    id: int
    brand: str
    model: int


class User(BaseModel):
    id: int
    name: str
    email: str


# Ejemplo de datos para carros y usuarios
cars: List[Car] = [
    Car(id=1, brand="Chevrolet", model=2009),
    Car(id=2, brand="Renault", model=2002)
]

users: List[User] = [
    User(id=1, name="Juan Santacruz", email="juan@gmail.com"),
    User(id=2, name="Mario Santacruz", email="mario@gmail.com"),
]


# Mostrar formulario para creación de un nuevo carro
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Endpoints para carros
@app.get("/cars", response_model=List[Car])
async def get_cars():
    return cars


@app.post("/cars", status_code=201)
async def create_car(request: Request, id: int = Form(...), brand: str = Form(...), model: int = Form(...)):
    cars.append(Car(id=id, brand=brand, model=model))
    return templates.TemplateResponse("index.html", {"request": request, "message": "Nuevo carro creado"})


@app.put("/cars/{car_id}")
async def update_car(car_id: int, updated_car: Car):
    for index, car in enumerate(cars):
        if car.id == car_id:
            cars[index] = updated_car
            return {"message": "Información del carro actualizada"}
    raise HTTPException(status_code=404, detail="Carro no encontrado")


@app.delete("/cars/{car_id}")
async def delete_car(car_id: int):
    for index, car in enumerate(cars):
        if car.id == car_id:
            cars.pop(index)
            return {"message": f"El carro con ID: {car_id} ha sido eliminado"}
    raise HTTPException(status_code=404, detail="Carro no encontrado")


# Endpoints para usuarios
@app.get("/users", response_model=List[User])
async def get_users():
    return users


@app.post("/users", status_code=201)
async def create_user(user: User):
    users.append(user)
    return {"message": "Nuevo usuario creado"}


@app.put("/users/{user_id}")
async def update_car(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return {"message": "Información del usuario actualizada"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete("/users/{user_id}")
async def delete_car(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return {"message": f"El usuario con ID: {user_id} ha sido eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
