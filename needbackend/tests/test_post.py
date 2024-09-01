from httpx import AsyncClient
from needbackend import models
import pytest

@pytest.mark.asyncio
async def test_no_permission_create_post_anonymous(
    client: AsyncClient, user1: models.DBUser,
):
    payload = {"content": "content anonymous", "user_id": user1.id,}
    response = await client.post("/posts/noauth", json=payload)

    data = response.json()

    assert response.status_code == 200
    assert data["content"] == payload["content"]
    assert data["id"] > 0
    assert data["user_id"] == user1.id
    assert data["completed"] == False

@pytest.mark.asyncio
async def test_no_permission_create_post(
    client: AsyncClient, user1: models.DBUser,
):
    payload = {"content": "content1", "user_id": user1.id,}
    response = await client.post("/posts", json=payload)

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_post_draft(
    client: AsyncClient,  token_user1: models.Token,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"content": "content1", "user_id": token_user1.user_id,}
    response = await client.post("/posts", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["content"] == payload["content"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id
    assert data["completed"] == False

@pytest.mark.asyncio
async def test_create_post_completed(
    client: AsyncClient,  token_user1: models.Token,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"content": "content1", "user_id": token_user1.user_id, "completed": True}
    response = await client.post("/posts", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["content"] == payload["content"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id
    assert data["completed"] == payload["completed"]

@pytest.mark.asyncio
async def test_list_post(client: AsyncClient, post_user1: models.DBPost,):
    response = await client.get("/posts")

    data = response.json()
    assert response.status_code == 200
    assert len(data["posts"]) > 0

    check_post = None
    for post in data["posts"]:
        if post["content"] == post_user1.content:
            check_post = post
            break
    
    
    assert check_post["id"] == post_user1.id
    assert check_post["content"] == post_user1.content
    assert check_post["completed"] == post_user1.completed
    assert check_post["create_at"] == post_user1.create_at.isoformat()

@pytest.mark.asyncio
async def test_id_post(client: AsyncClient, post_user1: models.DBPost,):
    response = await client.get(f"/posts/{post_user1.id}")

    data = response.json()

    assert data["id"] == post_user1.id
    assert data["content"] == post_user1.content
    assert data["completed"] == post_user1.completed
    assert data["create_at"] == post_user1.create_at.isoformat()

@pytest.mark.asyncio
async def test_no_permission_update_post(
    client: AsyncClient, post_user1: models.DBPost,
):
    padyload = payload = {"content": "content update", "completed": True}
    response = await client.put(
        f"/posts/{post_user1.id}", json=payload, 
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_post(
    client: AsyncClient,  token_user1: models.Token, post_user1: models.DBPost,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    padyload = payload = {"content": "content update", "user_id": token_user1.user_id, "completed": True}
    response = await client.put(
        f"/posts/{post_user1.id}", json=payload, headers=headers,
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == post_user1.id
    assert data["content"] == payload["content"]
    assert data["completed"] == payload["completed"]

@pytest.mark.asyncio
async def test_no_permission_delete_post(
    client: AsyncClient, post_user1: models.DBPost,
):
    response = await client.delete(
        f"/posts/{post_user1.id}", 
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_delete_post(
    client: AsyncClient, token_user1: models.Token, post_user1: models.DBPost,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.delete(
        f"/posts/{post_user1.id}", headers=headers,
    )

    data = response.json()
    
    assert data == {"message": "delete success"}