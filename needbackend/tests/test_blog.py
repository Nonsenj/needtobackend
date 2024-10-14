import pytest
from httpx import AsyncClient
from needbackend import models

@pytest.mark.asyncio
async def test_no_permission_create_blog(
    client: AsyncClient, user1: models.DBUser,
):
    payload = {"title": "Unauthorized Blog", "user_id": user1.id, "content": "Unauthorized content"}
    response = await client.post("/blogs", json=payload)

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_blog_non_tags(
    client: AsyncClient, token_user1: models.Token, user1: models.DBUser
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"title": "Draft Blog",
               "content": "Draft content", 
               "list_tags": [],
               }
    response = await client.post("/blogs", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id

@pytest.mark.asyncio
async def test_create_blog_with_tags(
    client: AsyncClient, token_user1: models.Token, tags1: models.DBTag
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"title": "Draft Blog",
               "content": "Draft content", 
               "list_tags": [{"name": tags1.name}],
               }
    response = await client.post("/blogs", json=payload, headers=headers)

    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id

@pytest.mark.asyncio
async def test_create_blog_with_new_tags(
    client: AsyncClient, token_user1: models.Token, tags1: models.DBTag
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"title": "Draft Blog",
               "content": "Draft content", 
               "list_tags": [{"name": "Game"}],
               }
    response = await client.post("/blogs", json=payload, headers=headers)

    data = response.json()
    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["id"] > 0
    assert data["user_id"] == token_user1.user_id

@pytest.mark.asyncio
async def test_list_blogs(client: AsyncClient, tags1: models.DBTag, blog_user1: models.DBBlog,):
    response = await client.get("/blogs")

    data = response.json()
    assert response.status_code == 200
    assert len(data["blogs"]) > 0

    check_blog = None
    for blog in data["blogs"]:
        if blog["title"] == blog_user1.title:
            check_blog = blog
            break

    assert check_blog["id"] == blog_user1.id
    assert check_blog["title"] == blog_user1.title
    assert check_blog["created_at"] == blog_user1.created_at.isoformat()
    assert check_blog["list_tags"][0]['name'] == tags1.name

@pytest.mark.asyncio
async def test_get_blog_by_id(client: AsyncClient, tags1: models.DBTag, blog_user1: models.DBBlog,):
    response = await client.get(f"/blogs/{blog_user1.id}/tag")

    data = response.json()
    assert data["id"] == blog_user1.id
    assert data["title"] == blog_user1.title
    assert data["content"] == blog_user1.content
    assert data["created_at"] == blog_user1.created_at.isoformat()
    assert data["list_tags"][0]["name"] == tags1.name

@pytest.mark.asyncio
async def test_get_blog_with_tag_comment(client: AsyncClient, tags1: models.DBTag, comment_blog_user1: models.DBCommentBlog, blog_user1: models.DBBlog,):
    response = await client.get(f"/blogs/{blog_user1.id}/tagcomment")

    data = response.json()
    assert data["id"] == blog_user1.id
    assert data["title"] == blog_user1.title
    assert data["content"] == blog_user1.content
    assert data["created_at"] == blog_user1.created_at.isoformat()
    assert data["list_tags"][0]["name"] == tags1.name
    assert data["comments"][0]["content"] == comment_blog_user1.content

@pytest.mark.asyncio
async def test_no_permission_update_blog(
    client: AsyncClient, blog_user1: models.DBBlog,
):
    payload = {"title": "Updated Blog", "content": "Updated content"}
    response = await client.put(
        f"/blogs/{blog_user1.id}", json=payload, 
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_blog(
    client: AsyncClient, token_user1: models.Token, blog_user1: models.DBBlog,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {"title": "Updated Blog", 
               "blogImage": "LinkImageBlog",
               "content": "Updated content", 
               }
    response = await client.put(
        f"/blogs/{blog_user1.id}", json=payload, headers=headers,
    )

    data = response.json()
    assert response.status_code == 200
    assert data["id"] == blog_user1.id
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]

@pytest.mark.asyncio
async def test_read_blog(
    client: AsyncClient, token_user1: models.Token, blog_user1: models.DBBlog,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.put(
        f"/blogs/{blog_user1.id}/read", headers=headers,
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == blog_user1.id
    assert data["title"] == blog_user1.title
    assert data["content"] == blog_user1.content
    assert data["reader"] > blog_user1.reader


@pytest.mark.asyncio
async def test_no_permission_delete_blog(
    client: AsyncClient, blog_user1: models.DBBlog,
):
    response = await client.delete(
        f"/blogs/{blog_user1.id}", 
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_delete_blog(
    client: AsyncClient, token_user1: models.Token, blog_user1: models.DBBlog,
):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.delete(
        f"/blogs/{blog_user1.id}", headers=headers,
    )

    data = response.json()
    
    assert data == {"message": "delete success"}
