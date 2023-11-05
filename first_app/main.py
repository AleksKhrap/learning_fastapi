from fastapi import FastAPI
from first_app.models.models import User, UserAdult, Feedback, UserCreate

app = FastAPI()

# Пример создания пользователя
user_data = {
    "id": 3,
    "name": "John Doe"
}
my_user = User(**user_data)


fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}


feedbacks = []
users = []


@app.get("/users")
async def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


# Эндпоинт для получения информации о пользователе по ID
@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.post("/users")
async def add_user(new_user: UserAdult):
    is_adult = True if new_user.age >= 18 else False
    return {
        "name": new_user.name,
        "age": new_user.age,
        "is_adult": is_adult
    }


@app.post("/feedback")
async def send_feedback(feedback: Feedback):
    feedbacks.append({
        "name": feedback.name,
        "message": feedback.message
    })
    return f"Feedback received. Thank you, {feedback.name}!"


@app.post("/create_user")
async def create_user(user: UserCreate) -> UserCreate:
    users.append(user)
    return user
