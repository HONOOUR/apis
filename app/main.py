from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from api.routes.todo import todo_router

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_header=["*"]
)

app.include_router(todo_router)
register_tortoise(
  app=app,
  db_url="sqlite://todo.db",
  add_exception_handlers=True,
  generate_schemas=True,
  modules={"models": ["api.models.todo"]}
)

class Item(BaseModel):
  text:str = None # validation
  is_done: bool = False
  
items = []

@app.get("/")
def root():
  return {"Hello" : "World"}

@app.post("/items")
def make_items(item: Item):
  items.append(item)
  return items

@app.get("/items", response_model=list[Item])  
def get_items(limit: int = 10):
  return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_items(item_id: int) -> Item:
  if item_id < len(items):
    return items[item_id]
  else:
    raise HTTPException(status_code=404, detail="Item not found")