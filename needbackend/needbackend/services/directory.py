import os

async def Create_Directory_User(name):
    static_dir = ".\static"

    if not os.path.exists(static_dir):
        os.mkdir(static_dir)

    user_dir = os.path.join(".\static", name)
    
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    
    return user_dir

async def Create_Directory_User(name):
    static_dir = ".\static"

    if not os.path.exists(static_dir):
        os.mkdir(static_dir)

    user_dir = os.path.join(".\static", name)
    
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    
    return user_dir
