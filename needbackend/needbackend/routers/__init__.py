from . import root
from . import users
from . import authentication
from . import post

from . import admins
from . import messages_router
from . import feeds
from . import blog
from . import group_chats_router
from . import individual_chats_router
from . import comment

def init_router(app):
    app.include_router(root.router)
    app.include_router(users.router)
    app.include_router(authentication.router)
    app.include_router(post.router)
    app.include_router(admins.router)
    app.include_router(messages_router.router)
    app.include_router(individual_chats_router.router)
    app.include_router(group_chats_router.router)
    app.include_router(feeds.router)
    app.include_router(blog.router)
    app.include_router(comment.router)

  
