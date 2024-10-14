import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from needbackend import models

@pytest.mark.asyncio
async def test_no_permission_get_me(client: AsyncClient, user1: models.DBUser):
    response = await client.get("/users/me")

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, token_user1: models.Token, user1: models.DBUser):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/users/me", headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["username"] == user1.username
    assert data["first_name"] == user1.first_name
    assert data["last_name"] == user1.last_name
    assert data["email"] == user1.email


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    payload = {
        "username": "new_user",
        "email": "new_user@example.com",
        "first_name": "New First",
        "last_name": "New Last",
        "password": "password123"
    }
    response = await client.post("/users/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, token_user1: models.Token,):
    headers = {"Authorization": f"Bearer {token_user1.access_token}"}
    payload = {
        "first_name": "Updated First",
        "last_name": "Updated Last",
        "email": "Updated@example.com",
    }
    response = await client.put(f"/users/update", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]

@pytest.mark.asyncio
async def test_change_password(client: AsyncClient, token_user1: models.Token, user1: models.DBUser):
    headers = {"Authorization": f"Bearer {token_user1.access_token}"}
    payload = {
        "current_password": "123456",
        "new_password": "new_password123"
    }
    response = await client.put(f"/users/{user1.id}/change_password", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Password updated successfully"

@pytest.mark.asyncio
async def test_list_users(client: AsyncClient,  user1: models.DBUser):
    response = await client.get("/users")

    data = response.json()
    assert response.status_code == 200
    assert len(data["users"]) > 0

    check_user= None
    for user in data["users"]:
        if user["username"] == user1.username:
            check_user = user
            break

    assert check_user["id"] == user1.id
    assert check_user["username"] == user1.username
    assert check_user["first_name"] == user1.first_name
    assert check_user["last_name"] == user1.last_name
    assert check_user["email"] == user1.email
    assert check_user["register_date"] == user1.register_date.isoformat()
