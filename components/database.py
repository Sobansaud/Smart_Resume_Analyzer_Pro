users_db = {
    "sobansaud3@gmail.com": {
        "name": "Soban Saud",
        "password": "soban123",  # In production, always hash passwords!
        "resumes": []
    }
}

def authenticate_user(email, password):
    user = users_db.get(email)
    if user and user["password"] == password:
        return user
    return None

def get_user(email):
    return users_db.get(email)

def save_resume(email, resume_data):
    if email in users_db:
        users_db[email]["resumes"].append(resume_data)
        return True
    return False
