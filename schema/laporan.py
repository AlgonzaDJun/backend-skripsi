# class Laporan(BaseModel):
#     judul: str
#     lokasi: str
#     fakultas: str
#     jurusan: str
#     deskripsi: str
#     status: str
#     gambar: List[str]
from .user import individual_serial as user_serial


def individual_serial(laporan) -> dict:
    return {
        "id": str(laporan["_id"]),
        "judul": laporan["judul"],
        "lokasi": laporan["lokasi"],
        "fakultas": laporan["fakultas"],
        "jurusan": laporan["jurusan"],
        "deskripsi": laporan["deskripsi"],
        "status": laporan["status"],
        "rating": laporan["rating"],
        "gambar": laporan["gambar"],
    }


def serial_with_user(laporan):
    return {
        "id": str(laporan["_id"]),
        "judul": laporan["judul"],
        "lokasi": laporan["lokasi"],
        "fakultas": laporan["fakultas"],
        "jurusan": laporan["jurusan"],
        "deskripsi": laporan["deskripsi"],
        "status": laporan["status"],
        "rating": laporan["rating"],
        "gambar": laporan["gambar"],
        "user_data": user_serial(laporan["user_data"]),
    }


def list_serial_with_user(laporans) -> list:
    return [serial_with_user(laporan) for laporan in laporans]


def list_serial(laporans) -> list:
    return [individual_serial(laporan) for laporan in laporans]
