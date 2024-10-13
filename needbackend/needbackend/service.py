import aiofiles
import os

async def create_directory(username: str):
    try:
        path = f"../uploads/{username}"
    
        if not os.path.exists(path):
            await aiofiles.os.makedirs(path)
        
        return f"{path}"
    except OSError as e:
        # Handle any errors that occur when creating the path
        print(f"Error creating path: {e}")
        return None
    except Exception as e:
        # Handle any other errors
        print(f"An error occurred: {e}")
        return None