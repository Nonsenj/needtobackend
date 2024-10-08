from .. import config
settings = config.get_settings()


async def Create_Path_Image(username, random_name):
    img_path = f"{settings.Server_URL}/file/image?id=./static/{username}/" + str(random_name) + ".jpg"
    return img_path