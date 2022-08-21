def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "aadhar": item["aadhar_no"],
        "phone": item["phone"],
        "udise": item["institute_id"],
        "tc": item["tc"]
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]