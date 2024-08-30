from . import root
from . import users
from . import authentication
from . import post

from . import admins
from . import messages
from . import groupchats
from . import individualchats
from . import feeds


def init_router(app):
    app.include_router(root.router)
    app.include_router(users.router)
    app.include_router(authentication.router)
    app.include_router(post.router)
    app.include_router(admins.router)
    app.include_router(messages.router)
    app.include_router(groupchats.router)
    app.include_router(individualchats.router)
    app.include_router(feeds.router)
  
