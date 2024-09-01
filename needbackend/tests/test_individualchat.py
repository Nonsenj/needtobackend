from httpx import AsyncClient
from needbackend import models
import pytest

@pytest.mark.asyncio
async def test_created_nopermission_individual_chat(
    client: AsyncClient, session: models.get_session, user1: models.DBUser, user2: models.DBUser
):
    payload = {
        "user1_id": user1.id,
        "user2_id": user2.id
    }
    response = await client.post("/individual_chats/", json=payload)

    assert response.status_code == 401