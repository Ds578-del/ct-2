from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Simple API Server")


items = []


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float


@app.get("/")
async def root():
    return {"message": "Welcome to the Simple API Server"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    if item.id is None:
        item.id = len(items) + 1
    items.append(item)
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            return items.pop(index)
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)