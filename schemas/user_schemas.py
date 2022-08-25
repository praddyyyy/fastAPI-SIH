def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "aadhar": item["aadhar_no"],
        "phone": item["phone"],
        "udise": item["institute_id"],
        "tc": item["tc"],
        "academic_details": item["academic_details"],
        "dob": item["birthdate"]
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

def aadhaarEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "aadhaar": item["aadhaar"],
        "name": item["name"],
        "phone": item["phone"]
    }

def aadhaarsEntity(entity) -> list:
    return [aadhaarEntity(item) for item in entity]