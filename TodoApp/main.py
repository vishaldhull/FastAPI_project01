from fastapi import FastAPI, Request
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="TodoApp/templates") 

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(todos.router, prefix="/todos", tags=["todos"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(users.router, prefix="/users", tags=["users"])