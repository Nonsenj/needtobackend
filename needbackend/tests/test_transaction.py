from httpx import AsyncClient
from digimon import models
import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_create_transaction(client: AsyncClient, token_user1: models.Token, item_user1: models.DBItem):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"item_id": item_user1.id, "user_id": token_user1.user_id}
    response = await client.post("/transactions", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 201
    assert data["id"] > 0
    assert data["item_id"] == payload["item_id"]
    assert data["user_id"] == payload["user_id"]

@pytest.mark.asyncio
async def test_read_transactions(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/transactions", headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert "transactions" in data
    assert "page" in data
    assert "page_count" in data
    assert "size_per_page" in data


@pytest.mark.asyncio
async def test_read_transaction(client: AsyncClient, token_user1: models.Token, transaction: models.DBTransaction):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get(f"/transactions/{transaction.id}", headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == transaction.id
    assert data["item_id"] == transaction.item_id
    assert data["user_id"] == transaction.user_id


@pytest.mark.asyncio
async def test_delete_transaction(client: AsyncClient, token_user1: models.Token, transaction: models.DBTransaction):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.delete(f"/transactions/{transaction.id}", headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert "delete success" in data["message"]