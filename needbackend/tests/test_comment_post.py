import pytest
from httpx import AsyncClient
from needbackend import models

@pytest.mark.asyncio
async def test_no_permission_create_post_comment(
    client: AsyncClient, 
    user1: models.DBUser, 
    post_user1: models.DBPost
):
    payload = {"content": "comment without permission", "user_id": user1.id, "post_id": post_user1.id}
    response = await client.post("/comments/post", json=payload)

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_post_comment(
    client: AsyncClient, 
    token_user1: models.Token, 
    post_user1: models.DBPost
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"content": "valid comment", "user_id": token_user1.user_id, "post_id": post_user1.id}
    response = await client.post("/comments/post", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["content"] == payload["content"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id
    assert data["post_id"] == post_user1.id

@pytest.mark.asyncio
async def test_get_post_comment_by_id(client: AsyncClient, comment_post_user1: models.DBCommentPost):
    response = await client.get(f"/comments/post/{comment_post_user1.id}")

    data = response.json()

    assert data["id"] == comment_post_user1.id
    assert data["content"] == comment_post_user1.content
    assert data["post_id"] == comment_post_user1.post_id

@pytest.mark.asyncio
async def test_no_permission_update_post_comment(
    client: AsyncClient, 
    comment_post_user1: models.DBCommentPost, 
    user1: models.DBUser, 
    post_user1: models.DBPost,
):
    payload = {"content": "Updated comment", "user_id": user1.id, "post_id": post_user1.id}
    response = await client.put(
        f"/comments/post/{comment_post_user1.id}", json=payload, 
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_post_comment(
    client: AsyncClient, 
    comment_post_user1: models.DBCommentPost, 
    token_user1: models.Token, 
    post_user1: models.DBPost,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"content": "Updated comment", "user_id": token_user1.user_id, "post_id": post_user1.id}
    response = await client.put(
        f"/comments/post/{comment_post_user1.id}", json=payload, headers=headers,
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == comment_post_user1.id
    assert data["content"] == payload["content"]
    assert data["user_id"] == token_user1.user_id
    assert data["post_id"] == post_user1.id

@pytest.mark.asyncio
async def test_no_permission_delete_post_comment(
    client: AsyncClient, comment_post_user1: models.DBCommentPost,
):
    response = await client.delete(
        f"/comments/post/{comment_post_user1.id}", 
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_post_comment(
    client: AsyncClient, 
    token_user1: models.Token, 
    comment_post_user1: models.DBCommentPost
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.delete(f"/comments/post/{comment_post_user1.id}", headers=headers)

    data = response.json()

    assert data == {"message": "delete success"}
