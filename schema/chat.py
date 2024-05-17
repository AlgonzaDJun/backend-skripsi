from .laporan import individual_serial as laporan_serial


def all_chat(chat) -> dict:
    return {
        "id": str(chat["_id"]),
        "laporan_id": str(chat["laporan_id"]),
        "judul": chat["laporan_data"]["judul"],
        "user_id": str(chat["user_id"]),
    }


def individual_serial(chat) -> dict:
    return {
        "id": str(chat["_id"]),
        "laporan_id": str(chat["laporan_id"]),
        "user_id": str(chat["user_id"]),
        "messages": list_serial_messages(chat["messages"]),
    }


def message_serial(chat) -> dict:
    return {
        "user_id": str(chat["user_id"]),
        "message": chat["message"],
        "time": chat["time"],
    }


def list_serial_messages(messages) -> list:
    return [message_serial(message) for message in messages]


def list_serial_detail(chats) -> list:
    return [all_chat(chat) for chat in chats]
