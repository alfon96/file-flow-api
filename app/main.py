from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI, WebSocket
from app.router.images import images_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.context import Context

app = FastAPI(description="File Flow API", version="0.0.1")

app.include_router(images_router, prefix="/api/v1/images", tags=["Images"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:5500"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Context()
    yield


@app.get("/", tags=["Root"])
def read_root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"])
async def server_status():
    return {"status": True}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
