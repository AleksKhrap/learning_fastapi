from fastapi import FastAPI, Cookie, Response
from first_app.models.models import User
import uuid

app = FastAPI()

sample_user: dict = {"username": "user123", "password": "password123"}
fake_db: list[User] = [User(**sample_user)]
sessions: dict = {}


@app.post("/login")
async def login(user: User, response: Response):
    for person in fake_db:
        if person.username == user.username and person.password == user.password:
            session_token = str(uuid.uuid4())
            sessions[session_token] = user  # сохранили в словаре сессию, токен - это ключ, а значение - объект юзера
            response.set_cookie(key="session_token", value=session_token, httponly=True)
            return {"message": "Cookie установлены"}
    return {"message": "Неверный логин или пароль"}


@app.get("/user")
async def user_info(session_token=Cookie()):
    user = sessions.get(session_token)
    if user:
        return user.model_dump()
    return {"message": "Не авторизован"}
