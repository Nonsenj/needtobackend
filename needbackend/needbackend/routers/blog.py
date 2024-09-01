# from fastapi import APIRouter, HTTPException, Depends, Query

# from typing import Optional, Annotated

# from sqlmodel import Field, SQLModel, Session, select, func
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlalchemy.orm import selectinload

# import math

# from .. import models
# from .. import deps

# router = APIRouter(prefix="/blogs", tags=["blogs"])

# SIZE_PER_PAGE = 50

# @router.get("")
# async def read_items(
#     session: Annotated[AsyncSession, Depends(models.get_session)],
#     page: int = 1,
# ) -> models.BlogList:
    
#     result = await session.exec(
#         select(models.DBBlog).where(models.DBBlog.completed == True)
#         .offset((page-1) * SIZE_PER_PAGE).limit(SIZE_PER_PAGE)
#     )

#     blogs = result.all()
#     page_count = int(
#         math.ceil(
#             (await session.exec(select(func.count(models.DBBlog.id)))).first()
#             / SIZE_PER_PAGE
#         )
#     )

#     return models.BlogList.model_validate(
#         dict(blogs=blogs, page_size=page_count, page=page, size_per_page=SIZE_PER_PAGE)
#     )

# @router.post("")
# async def create_blog(
#     blog: models.CreateBlog,
#     current_user: Annotated[models.users, Depends(deps.get_current_user)],
#     session: Annotated[AsyncSession, Depends(models.get_session)],
# ) -> models.Blog | None:
#     db_blog = models.DBBlog.model_validate(blog)
#     session.add(db_blog)
#     await session.commit()
#     await session.refresh(db_blog)
#     return  models.Blog.model_validate(db_blog)

# # @router.post("")
# # async def create_blog(
# #     session: Annotated[AsyncSession, Depends(models.get_session)],
# # ):
# #     test_tag = models.DBTag(name="test tag")

# #     test_blog = models.DBBlog(
# #         title= "test blog",
# #         author= "test author",
# #         list_tag= [test_tag]
# #     )

# #     session.add(test_blog)
# #     await session.commit()
# #     await session.refresh(test_blog)

# #     return models.Blog.model_validate(test_blog)
    

# # @router.get("/{blog_id}")
# # async def read_blog(
# #     blog_id: int,
# #     session:  Annotated[AsyncSession, Depends(models.get_session)],                            
# # ) -> models.Blog:
# #     db_blog = await session.get(models.DBBlog, blog_id)
# #     if db_blog:
# #         return models.Blog.model_validate(db_blog)
    
# #     raise HTTPException(status_code=404, detail="Blog not found")

# @router.get("/{blog_id}")
# async def read_blog(
#     blog_id: int,
#     session:  Annotated[AsyncSession, Depends(models.get_session)],                            
# ) -> models.Blog:
#     statement = select(models.DBBlog).where(models.DBBlog.id == blog_id)
#     result = await session.exec(statement)
#     db_blog = result.first()

#     if db_blog:
#         db_blog_with_tag = models.Blog(
#             id=db_blog.id,
#             title=db_blog.title,
#             author=db_blog.author,
#             content=db_blog.content,
#             subtitle=db_blog.subtitle,
#             completed=db_blog.completed,
#             created_at=db_blog.created_at,
#             tags= [models.DBTag(id=tag.id, name=tag.name) for tag in db_blog.list_tag]
            
#         )
#         return db_blog_with_tag
    
#     raise HTTPException(status_code=404, detail="Blog not found")

# @router.put("/{blog_id}")
# async def update_blog(
#     blog_id: int,
#     blog: models.UpdataBlog,
#     current_user: Annotated[models.users, Depends(deps.get_current_user)],
#     session:  Annotated[AsyncSession, Depends(models.get_session)], 
# ) -> models.Blog:
#     data = blog.model_dump()
#     db_blog = await session.get(models.DBBlog, blog_id)
#     db_blog.sqlmodel_update(data)
#     session.add(db_blog)
#     await session.commit()
#     await session.refresh(db_blog)

#     return models.Blog.model_validate(db_blog)

# @router.delete("/{blog_id}")
# async def delete_blog(
#     blog_id: int,
#     current_user: Annotated[models.users, Depends(deps.get_current_user)],
#     session:  Annotated[AsyncSession, Depends(models.get_session)], 
# ) -> dict:
#     db_blog = await session.get(models.DBBlog, blog_id)
#     await session.delete(db_blog)
#     await session.commit()

#     return dict(message="delete success")
    