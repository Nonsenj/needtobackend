from fastapi import APIRouter, Depends, HTTPException, Request, status, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/websockets", tags=["websockets"])
templates = Jinja2Templates(directory="templates")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

@router.get("/", response_class=HTMLResponse)
def read_html(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})