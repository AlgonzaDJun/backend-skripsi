from fastapi import APIRouter, HTTPException
from models.todos import Todo
from config.database import todo_collection
from schema.todo import list_serial
from bson import ObjectId
from .todo_router import router as todo_router
from .user_router import router as user_router
from .laporan_router import router as laporan_router
from .chat_rotuer import router as chat_router

router = APIRouter()

router.include_router(todo_router, prefix="/todo", tags=["todo"])
router.include_router(user_router, prefix="/auth", tags=["auth"])
router.include_router(laporan_router, prefix="/laporan", tags=["laporan"])
router.include_router(chat_router, prefix="/chat", tags=["chat"])
