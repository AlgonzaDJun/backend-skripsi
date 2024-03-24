def individual_serial(user) -> dict:
    # full_name: str
    # prodi: str
    # fakultas: str
    # nim: str
    # username: str
    # password: str
    # email: str
    # no_hp: str
    # role: str = "user"
    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "prodi": user["prodi"],
        "fakultas": user["fakultas"],
        "nim": user["nim"],
        "username": user["username"],
        "password": user["password"],
        "email": user["email"],
        "role": user["role"],
    }


def list_serial(users) -> list:
    return [individual_serial(user) for user in users]
