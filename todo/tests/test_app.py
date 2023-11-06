from app.main import app
from httpx import AsyncClient


async def test_read_todos():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/todos")
    assert response.status_code == 200


"""async def test_add_todo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        mock_todo = {
            "title": "Test Todo",
            "description": "This is a test todo."
        }
        response = await ac.post("/todos/add_todo", json=mock_todo)
    assert response.status_code == 200
    assert response.json()"""
