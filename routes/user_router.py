from fastapi import APIRouter, HTTPException
from models.users import User, Login
from config.database import user_collection, laporan_collection
from passlib.context import CryptContext
from bson import ObjectId

# from typing import List
from schema.user import list_serial, individual_serial

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register")
async def create_user(user: User):

    # cek email and username
    if user_collection.find_one({"email": user.email}):
        return HTTPException(status_code=400, detail="Email already registered")

    if user_collection.find_one({"username": user.username}):
        return HTTPException(status_code=400, detail="Username already registered")

    # hash password
    user.password = get_password_hash(user.password)
    new_user = user_collection.insert_one(dict(user))
    if new_user.inserted_id:
        return {"message": "User created successfully", "data": dict(user)}
    else:
        return HTTPException(status_code=500, detail="Failed to create user")


@router.post("/login")
async def login(login: Login):
    user = user_collection.find_one(
        {"$or": [{"username": login.username}, {"email": login.username}]}
    )
    if not user:
        return HTTPException(status_code=404, detail="User not found")

    user_data = User(**user)

    if not verify_password(login.password, user_data.password):
        return HTTPException(status_code=400, detail="Invalid password")

    return {
        "message": "Login success",
        "data": individual_serial(user),
    }


@router.get("/user")
def read_users():
    users = list_serial(user_collection.find())
    return users


@router.get("/dashboard-admin")
def read_dashboard_admin():
    laporan_diajukan = laporan_collection.count_documents({"status": "diajukan"})
    laporan_ditangani = laporan_collection.count_documents({"status": "ditangani"})
    laporan_ditolak = laporan_collection.count_documents({"status": "ditolak"})
    return {
        "message": "Data dashboard admin berhasil didapatkan",
        "data": {
            "laporan_diajukan": laporan_diajukan,
            "laporan_ditangani": laporan_ditangani,
            "laporan_ditolak": laporan_ditolak,
        },
    }


@router.get("/{user_id}")
def read_user(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"message": "User found", "data": individual_serial(user)}
    else:
        return HTTPException(status_code=404, detail="User not found")
