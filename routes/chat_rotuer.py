from fastapi import APIRouter, HTTPException
from typing import List
from models.chat import Chat, ChatDB
from config.database import chat_collection, user_collection
from bson import ObjectId
from datetime import datetime
from schema.chat import individual_serial, list_serial_detail
import pusher


pusher_client = pusher.Pusher(
    app_id="1788134",
    key="1878dcbb07e22275630e",
    secret="708f2fc8c2f447d11006",
    cluster="ap1",
    ssl=True,
)


router = APIRouter()


@router.get("/")
async def get_all_chat_admin():
    chats = chat_collection.aggregate(
        [
            {
                "$lookup": {
                    "from": "laporans",
                    "localField": "laporan_id",
                    "foreignField": "_id",
                    "as": "laporan_data",
                }
            },
            {"$unwind": "$laporan_data"},
        ]
    )
    allchat = list(chats)
    allchat = list_serial_detail(allchat)
    return {"messages": "chat berhasil ditemukan", "data": allchat}


@router.get("/{user_id}")
async def get_all_chat(user_id: str):
    chats = chat_collection.aggregate(
        [
            {
                "$lookup": {
                    "from": "laporans",
                    "localField": "laporan_id",
                    "foreignField": "_id",
                    "as": "laporan_data",
                }
            },
            {"$unwind": "$laporan_data"},
            {"$match": {"user_id": ObjectId(user_id)}},
        ]
    )
    allchat = list(chats)
    allchat = list_serial_detail(allchat)
    # print(allchat)

    return {"messages": "chat berhasil ditemukan", "data": allchat}


@router.get("/{laporan_id}/{user_id}")
async def get_chat_by_room(laporan_id: str, user_id: str):
    chat = chat_collection.find_one(
        {"laporan_id": ObjectId(laporan_id), "user_id": ObjectId(user_id)}
    )
    chats = individual_serial(chat)
    return {"messages": "chat berhasil ditemukan", "data": chats}


@router.post("/")
async def add_chat(chat: Chat):
    try:
        channel = chat.laporan_id + "-" + chat.user_id
        admin = user_collection.find_one({"role": "admin"})

        if chat.sender == "admin":
            pusher_client.trigger(
                channel,
                "my-event",
                {"message": chat.messages, "user_id": str(admin["_id"])},
            )
        else:
            pusher_client.trigger(
                channel, "my-event", {"message": chat.messages, "user_id": chat.user_id}
            )

        user_id = chat.user_id

        if chat.sender == "admin":
            user_id = admin["_id"]

        # jika ada laporan maka tambahkan chat, jika belum ada maka buat chat baru
        laporan = chat_collection.find_one(
            {"laporan_id": ObjectId(chat.laporan_id), "user_id": ObjectId(chat.user_id)}
        )
        if laporan:
            chat_collection.update_one(
                {
                    "laporan_id": ObjectId(chat.laporan_id),
                    "user_id": ObjectId(chat.user_id),
                },
                {
                    "$push": {
                        "messages": {
                            "user_id": ObjectId(user_id),
                            "message": chat.messages,
                            "time": datetime.now(),
                        }
                    }
                },
            )
            return {"message": "chat added successfully"}
        else:
            chat_collection.insert_one(
                {
                    "laporan_id": ObjectId(chat.laporan_id),
                    "user_id": ObjectId(chat.user_id),
                    "messages": [
                        {
                            "user_id": ObjectId(user_id),
                            "message": chat.messages,
                            "time": datetime.now(),
                        }
                    ],
                }
            )
            return {"message": "chat created successfully"}
    except Exception as e:
        return {"message": str(e)}
