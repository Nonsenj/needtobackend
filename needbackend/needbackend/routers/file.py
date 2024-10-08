from fastapi import APIRouter, Depends, HTTPException, Request, status, File, UploadFile
import uuid
import os
import base64
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from ..services import directory
from .. import models
from .. import deps

router = APIRouter(prefix="/file", tags=["File"])

@router.post("/upload_image")
async def convert_image(file: UploadFile,
    current_user: models.User = Depends(deps.get_current_user),
    ):
    path = await directory.Create_Directory_User(current_user.username)
    random_name = str(uuid.uuid4())
    decodeit = open(f"{path}/Profile_{random_name}.jpg", 'wb')
    contents = await file.read()
    decodeit.write(contents)
    img_path = f"http://localhost:8000/file/images?id=./static/{current_user.username}/" + str(random_name) + ".jpg"

    return {"image_url": img_path}

@router.get("/image")
async def get_image_id(id: str):
    return FileResponse(id)

@router.get("")
async def get_images():
    path = "./static/admin"
    files = os.listdir(path)
    file_list = [f for f in files if os.path.isfile(os.path.join(path, f))]
    return JSONResponse(content={"files": file_list})