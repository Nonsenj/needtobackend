from . import root
from . import users
from . import authentication
from . import admins
from . import messages

def init_router(app):
    app.include_router(root.router)
    app.include_router(users.router)
    app.include_router(authentication.router)
    app.include_router(admins.router)
    app.include_router(messages.router)