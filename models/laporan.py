from pydantic import BaseModel
from typing import List
from bson import ObjectId


class Laporan(BaseModel):
    user_id: str
    judul: str
    lokasi: str
    fakultas: str
    jurusan: str
    deskripsi: str
    status: str = "diajukan"
    rating: int = 0
    gambar: List[str]


class Text(BaseModel):
    text: str
