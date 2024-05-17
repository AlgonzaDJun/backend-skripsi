from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from models.laporan import Laporan, Text
from config.database import laporan_collection
from schema.laporan import list_serial, individual_serial, list_serial_with_user
from bson import ObjectId
import cloudinary
import cloudinary.uploader
import cloudinary.api

from utils.clustering_utils import (
    perform_clustering_dev,
    perform_ner,
    find_optimal_num_clusters_silhouette,
    find_optimal_num_clusters_silhouette_chart,
)

from utils.summarize import summarize_text_online, summarize_text_offline

router = APIRouter()

CLOUDINARY_URL = "cloudinary://845972999637854:c85t26oCN-NvsmPaXbFYc8nANSE@diavohz3e"

cloudinary.config(
    cloud_name="diavohz3e",
    api_key="845972999637854",
    api_secret="c85t26oCN-NvsmPaXbFYc8nANSE",
    secure=True,
)


# POST LAPORAN BARU
@router.post("/")
async def post_laporan(laporan: Laporan):

    laporan.user_id = ObjectId(laporan.user_id)
    if laporan.gambar:
        laporan.gambar = [
            cloudinary.uploader.upload(
                img,
                folder="laporan_skripsi",
            )["secure_url"]
            for img in laporan.gambar
        ]

    new_laporan = laporan_collection.insert_one(dict(laporan))
    if new_laporan.inserted_id:
        return {
            "message": "Laporan berhasil dibuat",
            # "data": dict(laporan),
        }
    else:
        raise HTTPException(status_code=500, detail="Gagal membuat laporan")


# get all laporan
@router.get("/")
async def get_laporans():
    try:
        laporans = laporan_collection.aggregate(
            [
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "user_id",
                        "foreignField": "_id",
                        "as": "user_data",
                    }
                },
                {"$unwind": "$user_data"},
            ]
        )
        laporans = list(laporans)

        return {
            "message": "Data laporan berhasil didapatkan",
            "data": list_serial_with_user(laporans),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/user/{user_id}")
async def get_laporans_by_user_id(user_id):
    try:
        laporans = laporan_collection.find({"user_id": ObjectId(user_id)})
        laporans = list(laporans)

        return {
            "message": "Data laporan berhasil didapatkan",
            "data": list_serial(laporans),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


import json


@router.get("/cluster")
async def cluster_laporan(jumlah_cluster: int = 5):
    try:
        laporans = laporan_collection.find({"status": {"$nin": ["selesai", "ditolak"]}})
        laporans = list(laporans)

        # # Mengambil data laporan yang memiliki gambar
        # laporans_with_image = [lap for lap in laporans if "gambar" in lap]

        # # Mengambil url gambar dari laporan
        # image_urls = [lap["gambar"] for lap in laporans_with_image]

        # # Melakukan clustering
        # data = [
        #     {
        #         "_id": 1,
        #         "judul": "Kursi food court sering patah",
        #         "deskripsi": "Kursi di food court danau unesa sering patah.",
        #         "fakultas": "-",
        #         "jurusan": "-",
        #         "lokasi": "Food Court Danau Unesa Ketintang",
        #         "gambar": "-",
        #         "status": "-",
        #     },
        #     {
        #         "_id": 2,
        #         "judul": "kursi di food court",
        #         "deskripsi": "Kursi di food court danau unesa sudah sangat usang.",
        #         "fakultas": "-",
        #         "jurusan": "-",
        #         "lokasi": "Food Court Danau Unesa Ketintang",
        #         "gambar": "-",
        #         "status": "-",
        #     },
        #     {
        #         "_id": 3,
        #         "judul": "Tempat duduk tidak nyaman di food court danau unesa",
        #         "deskripsi": "tempat duduk di food court danau unesa tidak nyaman.",
        #         "fakultas": "-",
        #         "jurusan": "-",
        #         "lokasi": "Food Court Danau Unesa Ketintang",
        #         "gambar": "-",
        #         "status": "-",
        #     },
        #     {
        #         "_id": 4,
        #         "judul": "Kursi food court perlu diperbaiki",
        #         "deskripsi": "Kursi di food court perlu diperbaiki.",
        #         "fakultas": "-",
        #         "jurusan": "-",
        #         "lokasi": "Food Court Danau Unesa Ketintang",
        #         "gambar": "-",
        #         "status": "-",
        #     },
        #     {
        #         "_id": 5,
        #         "judul": "tempat sampah penuh",
        #         "deskripsi": "Saya menemukan tempat sampah yang penuh di food court.",
        #         "fakultas": "-",
        #         "jurusan": "-",
        #         "lokasi": "Food Court Danau Unesa Ketintang",
        #         "gambar": "-",
        #         "status": "-",
        #     },
        #     {
        #         "_id": 6,
        #         "judul": "Banyak sampah di sekitar danau unesa",
        #         "deskripsi": "Saya menemukan banyak sampah di sekitar danau unesa.",
        #         "fakultas": "-",
        #         "jurusan": "-",
        #         "lokasi": "Food Court Danau Unesa Ketintang",
        #         "gambar": "-",
        #         "status": "-",
        #     },
        #     {
        #         "_id": 7,
        #         "judul": "tempat sampah di food court",
        #         "deskripsi": "Tempat sampah di food court danau unesa penuh.",
        #         "fakultas": "-",
        #         "jurusan": "-",
        #         "lokasi": "Food Court Danau Unesa Ketintang",
        #         "gambar": "-",
        #         "status": "-",
        #     },
        # ]

        clusters = perform_clustering_dev(laporans, jumlah_cluster)
        # print(clusters)

        # Menggabungkan hasil clustering dengan data laporan
        # for i, lap in enumerate(laporans_with_image):
        #     lap["cluster"] = clusters[i]

        return {
            "message": "Data laporan berhasil didapatkan",
            "data": clusters,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/ner")
async def ner_laporan(jumlah_cluster: int = 5):
    try:
        laporans = laporan_collection.find({"status": {"$nin": ["selesai", "ditolak"]}})
        laporans = list(laporans)

        # # Mengambil data laporan yang memiliki gambar
        # laporans_with_image = [lap for lap in laporans if "gambar" in lap]

        # # Mengambil url gambar dari laporan
        # image_urls = [lap["gambar"] for lap in laporans_with_image]

        # # Melakukan clustering
        clusters = perform_ner(laporans, jumlah_cluster)
        # print(clusters)

        # Menggabungkan hasil clustering dengan data laporan
        # for i, lap in enumerate(laporans_with_image):
        #     lap["cluster"] = clusters[i]

        return {
            "message": "Data laporan berhasil didapatkan",
            "data": clusters,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/shilouette-score")
async def get_shilouette_score(jumlah_cluster: int = 10):
    try:
        laporans = laporan_collection.find({})
        laporans = list(laporans)

        # # Mengambil data laporan yang memiliki gambar
        # laporans_with_image = [lap for lap in laporans if "gambar" in lap]

        # # Mengambil url gambar dari laporan
        # image_urls = [lap["gambar"] for lap in laporans_with_image]

        # # Melakukan clustering
        clusters = find_optimal_num_clusters_silhouette(laporans, jumlah_cluster)
        # print(clusters)

        # Menggabungkan hasil clustering dengan data laporan
        # for i, lap in enumerate(laporans_with_image):
        #     lap["cluster"] = clusters[i]

        return {
            "message": "Data Shilouette berhasil didapatkan",
            "data": clusters,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/shilouette-chart", response_class=HTMLResponse)
async def get_shilouette_chart():
    try:
        laporans = laporan_collection.find({})
        laporans = list(laporans)

        # # Mengambil data laporan yang memiliki gambar
        # laporans_with_image = [lap for lap in laporans if "gambar" in lap]

        # # Mengambil url gambar dari laporan
        # image_urls = [lap["gambar"] for lap in laporans_with_image]

        # # Melakukan clustering
        clusters = find_optimal_num_clusters_silhouette_chart(laporans)
        # print(clusters)

        # Menggabungkan hasil clustering dengan data laporan
        # for i, lap in enumerate(laporans_with_image):
        #     lap["cluster"] = clusters[i]

        return HTMLResponse(content=clusters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/summarize-text")
async def get_summary(text: Text):
    try:
        # get text.text
        text = text.text
        sum_text = summarize_text_online(text)

        return {
            "message": "Summarize text berhasil didapatkan",
            "data": sum_text,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/{id}")
async def get_laporan_by_id(id):
    try:
        laporan = laporan_collection.find_one({"_id": ObjectId(id)})
        return {
            "message": "Data laporan berhasil didapatkan",
            "data": individual_serial(laporan),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/insert-many")
async def insert_many_laporan(laporan: list[Laporan]):
    try:
        # laporan = [dict(lap) for lap in laporan]
        # new_laporan = laporan_collection.insert_many(laporan)

        for lap in laporan:
            lap.user_id = ObjectId(lap.user_id)

        # Mengonversi list Laporan menjadi list dictionary
        laporan_dict_list = [dict(lap) for lap in laporan]

        # Menyimpan data ke MongoDB menggunakan insert_many
        new_laporan = laporan_collection.insert_many(laporan_dict_list)
        if new_laporan.inserted_ids:
            return {
                "message": "Laporan berhasil dibuat",
                # "data": new_laporan.inserted_ids,
            }
        else:
            raise HTTPException(status_code=500, detail="Gagal membuat laporan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# edit many by id
@router.put("/edit-many")
async def edit_many_laporan(ids: list[str], new_status: str):
    try:
        object_ids = [ObjectId(id) for id in ids]

        # Update data for each ID
        for object_id in object_ids:
            # Fetch existing data
            existing_data = laporan_collection.find_one({"_id": object_id})
            if existing_data:
                # Update existing data
                existing_data["status"] = new_status
                # Perform update operation
                laporan_collection.update_one(
                    {"_id": object_id}, {"$set": {"status": new_status}}
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Laporan dengan ID {str(object_id)} tidak ditemukan",
                )

        return {"message": "Status berhasil diubah"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.put("/status/{id}")
async def edit_status(id, new_status):
    try:
        laporan_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": {"status": new_status}},
        )

        return {
            "message": "Status berhasil diubah",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    # @router.put("/{id}")
    # async def edit_laporan(id, laporan: Laporan):
    try:
        laporan.user_id = ObjectId(laporan.user_id)
        if laporan.gambar:
            laporan.gambar = [
                cloudinary.uploader.upload(
                    img,
                    folder="laporan_skripsi",
                )["secure_url"]
                for img in laporan.gambar
            ]

        updated_laporan = laporan_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": dict(laporan)}
        )
        if updated_laporan.modified_count:
            return {
                "message": "Laporan berhasil diubah",
                # "data": dict(laporan),
            }
        else:
            raise HTTPException(status_code=500, detail="Gagal mengubah laporan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/rating/{id}")
async def post_rating(id: str, rating: int):
    try:
        updated_laporan = laporan_collection.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": {"rating": rating}}
        )
        if updated_laporan:
            return {
                "message": "Rating berhasil ditambahkan",
            }
        else:
            raise HTTPException(status_code=500, detail="Gagal menambahkan rating")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
