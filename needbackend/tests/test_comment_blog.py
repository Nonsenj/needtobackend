import pytest
from httpx import AsyncClient
from needbackend import models

@pytest.mark.asyncio
async def test_no_permission_create_blog_comment(
    client: AsyncClient, user1: models.DBUser, blog_user1: models.DBBlog
):
    payload = {"content": "comment without permission", "user_id": user1.id, "blog_id": blog_user1.id}
    response = await client.post("/comments/blog", json=payload)

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_blog_comment(
    client: AsyncClient, token_user1: models.Token, blog_user1: models.DBBlog
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"content": "valid blog comment", "user_id": token_user1.user_id, "blog_id": blog_user1.id}
    response = await client.post("/comments/blog", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["content"] == payload["content"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id
    assert data["blog_id"] == blog_user1.id

@pytest.mark.asyncio
async def test_get_blog_comment_by_id(client: AsyncClient, comment_blog_user1: models.DBCommentBlog):
    response = await client.get(f"/comments/blog/{comment_blog_user1.id}")

    data = response.json()

    assert data["id"] == comment_blog_user1.id
    assert data["content"] == comment_blog_user1.content
    assert data["blog_id"] == comment_blog_user1.blog_id

@pytest.mark.asyncio
async def test_no_permission_update_blog_comment(
    client: AsyncClient, 
    comment_blog_user1: models.DBCommentBlog,
    user1: models.DBUser, 
    blog_user1: models.DBBlog,
):
    payload = {"content": "Updated comment", "user_id": user1.id, "blog_id": blog_user1.id}
    response = await client.put(
        f"/comments/blog/{comment_blog_user1.id}", json=payload, 
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_blog_comment(
    client: AsyncClient, 
    comment_blog_user1: models.DBCommentBlog,
    token_user1: models.Token, 
    blog_user1: models.DBBlog,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"content": "Updated comment", "user_id": token_user1.user_id, "blog_id": blog_user1.id}
    response = await client.put(
        f"/comments/blog/{comment_blog_user1.id}", json=payload, headers=headers,
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == comment_blog_user1.id
    assert data["content"] == payload["content"]
    assert data["user_id"] == token_user1.user_id
    assert data["blog_id"] == blog_user1.id

@pytest.mark.asyncio
async def test_no_permission_delete_blog_comment(
    client: AsyncClient, comment_blog_user1: models.DBCommentBlog,
):
    response = await client.delete(
        f"/comments/blog/{comment_blog_user1.id}", 
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_delete_blog_comment(
    client: AsyncClient, token_user1: models.Token, comment_blog_user1: models.DBCommentBlog,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.delete(f"/comments/blog/{comment_blog_user1.id}", headers=headers)

    data = response.json()

    assert data == {"message": "delete success"}
