from typing import Union
from fastapi import FastAPI, WebSocket
from app.router.images import images_router
from fastapi.responses import RedirectResponse

app = FastAPI(description="File Flow API", version="0.0.1")

app.include_router(images_router, prefix="/api/v1/images", tags=["images"])


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
async def server_status():
    return {"status": True}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
