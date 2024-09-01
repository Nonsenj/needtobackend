from . import root
from . import users
from . import authentication


from . import admins
from . import messages_chat_router
from . import messages_group_router
from . import group_chats_router
from . import individual_chats_router
from . import blog
from . import comment
from . import feeds
from . import post

def init_router(app):
    app.include_router(root.router)
    app.include_router(users.router)
    app.include_router(authentication.router)
    app.include_router(admins.router)
    app.include_router(messages_chat_router.router)
    app.include_router(messages_group_router.router)
    app.include_router(individual_chats_router.router)
    app.include_router(group_chats_router.router)
    app.include_router(blog.router)
    app.include_router(comment.router)
    app.include_router(feeds.router)
    app.include_router(post.router)


  
