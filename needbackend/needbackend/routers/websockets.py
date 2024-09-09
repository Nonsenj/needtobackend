from fastapi import APIRouter, Depends, HTTPException, Request, status, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/websockets", tags=["websockets"])
templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, room_id: int):
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:
            del self.active_connections[room_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str, room_id: int, websocket: WebSocket):
        for connection in self.active_connections.get(room_id, []):
            if websocket != connection:
                await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, client_id: int):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} in room {room_id} says: {data}", room_id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast(f"Client #{client_id} left room {room_id}", room_id)

@router.get("/", response_class=HTMLResponse)
def read_html(request: Request):
    return templates.TemplateResponse("room.html", {"request": request})