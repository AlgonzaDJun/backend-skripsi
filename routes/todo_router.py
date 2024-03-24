from fastapi import APIRouter, HTTPException
from models.todos import Todo
from config.database import todo_collection
from schema.todo import list_serial
from bson import ObjectId

router = APIRouter()


# GET
@router.get("/")
async def get_todos():
    todos = list_serial(todo_collection.find())
    return todos


@router.post("/")
async def post_todo(todo: Todo):
    new_todo = todo_collection.insert_one(dict(todo))
    if new_todo.inserted_id:
        return {"message": "Todo created successfully", "new_todo": dict(todo)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create todo")


@router.put("/{id}")
async def put_todo(id: str, todo: Todo):
    todo_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(todo)})
    return {"message": "Todo has been updated successfully", "new_todo": dict(todo)}


@router.delete("/{id}")
async def delete_todo(id: str):
    todo_collection.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "Todo has been deleted successfully"}
