from fastapi import FastAPI,HTTPException
from typing import List
from models import User, Gender, Role, UserUpdateRequest
from uuid import UUID

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("1bc3e83f-fee3-443e-a1a7-11ffac164efe"),
        first_name="Kagiso",
        last_name= "Mphayi",
        gender= Gender.male, 
        roles=[Role.student]
    ),
    User(
        id=UUID("3b46ce69-97c5-4f5e-87b0-1d20325a2644"),
        first_name="William",
        last_name= "Jones",
        gender= Gender.female,
        roles=[Role.admin, Role.user] 
    )
]

@app.get("/")
async def root():
    return{"Hello": "Kagiso"}

@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return("User deleted")
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name               
            if user_update.roles is not None:
                user.roles = user_update.roles
            return            
    raise HTTPException(status_code=404, detail="User with id: {user_id} does not exist")

        