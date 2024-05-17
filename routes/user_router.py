from fastapi import APIRouter, HTTPException
from models.users import User, Login
from config.database import user_collection, laporan_collection
from passlib.context import CryptContext
from bson import ObjectId
import requests
import re

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

    cek_pddikti = await check_user_api(user.nim)
    full_name = user.full_name

    if cek_pddikti.lower() != full_name.lower():
        raise HTTPException(
            status_code=500,
            detail="Nama Lengkap anda tidak sesuai dengan database PDDIKTI",
        )
    # else:
    #     return {"message": "User created"}

    # return {
    #     "message": "User created successfully",
    # }

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
    laporan_selesai = laporan_collection.count_documents({"status": "selesai"})
    laporan_ditolak = laporan_collection.count_documents({"status": "ditolak"})
    laporan_per_fakultas = laporan_collection.aggregate(
        [
            {
                "$group": {
                    "_id": "$fakultas",
                    "total": {"$sum": 1},
                }
            }
        ]
    )
    laporan_per_fakultas_dan_status = laporan_collection.aggregate(
        [
            {
                "$group": {
                    "_id": {"fakultas": "$fakultas", "status": "$status"},
                    "total": {"$sum": 1},
                }
            },
            {
                "$group": {
                    "_id": "$_id.fakultas",
                    "status_counts": {
                        "$push": {"status": "$_id.status", "count": "$total"}
                    },
                    "total": {"$sum": "$total"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "fakultas": "$_id",
                    "status_counts": 1,
                    "total": 1,
                }
            },
        ]
    )
    laporan_per_jurusan = laporan_collection.aggregate(
        [
            {
                "$group": {
                    "_id": "$jurusan",
                    "total": {"$sum": 1},
                }
            }
        ]
    )
    return {
        "message": "Data dashboard admin berhasil didapatkan",
        "data": {
            "laporan_diajukan": laporan_diajukan,
            "laporan_selesai": laporan_selesai,
            "laporan_ditolak": laporan_ditolak,
            "laporan_per_fakultas": list(laporan_per_fakultas),
            "laporan_per_jurusan": list(laporan_per_jurusan),
            "laporan_per_fakultas_dan_status": list(laporan_per_fakultas_dan_status),
        },
    }


async def check_user_api(user_id: str):
    url_dosen = "https://api-frontend.kemdikbud.go.id/hit/"
    url_mhs = "https://api-frontend.kemdikbud.go.id/hit_mhs/"
    response_dosen = requests.get(url_dosen + user_id)
    response_mhs = requests.get(url_mhs + user_id)

    dosen_data = response_dosen.json()
    mhs_data = response_mhs.json()
    # bu anit 0025016903
    # pak ricky 0716018704
    nama_dosen = dosen_data.get("dosen")[0]["text"]
    nama_mhs = mhs_data.get("mahasiswa")[0]["text"]

    split_dosen = re.split(r"\s*,\s*", nama_dosen)
    split_mhs = re.search(r"^[^()]+", nama_mhs)

    nama_asli_dosen = split_dosen[0]
    nama_asli_mhs = split_mhs.group(0)

    if nama_asli_dosen != f"Cari kata kunci {user_id} pada Data Dosen":
        return nama_asli_dosen
    elif nama_asli_mhs != f"Cari kata kunci {user_id} pada Data Mahasiswa":
        return nama_asli_mhs
    else:
        return "Nama tidak ditemukan"


@router.get("/{user_id}")
def read_user(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"message": "User found", "data": individual_serial(user)}
    else:
        return HTTPException(status_code=404, detail="User not found")
