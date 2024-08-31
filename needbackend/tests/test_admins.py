import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from needbackend import models

@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, token_admin1: models.Token):
    headers = {"Authorization": f"Bearer {token_admin1.access_token}"}
    response = await client.get("/admins/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == token_admin1.user.username

@pytest.mark.asyncio
async def test_get_admin(client: AsyncClient, admin1: models.DBUser):
    response = await client.get(f"/admins/{admin1.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == admin1.username

@pytest.mark.asyncio
async def test_create_admin(client: AsyncClient):
    payload = {
        "username": "new_admin",
        "email": "new_admin@example.com",
        "first_name": "New",
        "last_name": "Admin",
        "password": "password123"
    }
    response = await client.post("/admins/create", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]

@pytest.mark.asyncio
async def test_update_admin(client: AsyncClient, token_admin1: models.Token, admin1: models.DBUser):
    headers = {"Authorization": f"Bearer {token_admin1.access_token}"}
    payload = {
        "first_name": "Updated",
        "last_name": "Admin"
    }
    response = await client.put(f"/admins/{admin1.id}/update", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == payload["first_name"]

@pytest.mark.asyncio
async def test_change_password(client: AsyncClient, token_admin1: models.Token, admin1: models.DBUser):
    headers = {"Authorization": f"Bearer {token_admin1.access_token}"}
    payload = {
        "current_password": "password123",
        "new_password": "new_password123"
    }
    response = await client.put(f"/admins/{admin1.id}/change_password", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Password updated successfully"