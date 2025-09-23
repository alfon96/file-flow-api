from typing import Union
from fastapi import FastAPI, File, UploadFile
from typing import Annotated
from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl


images_router = APIRouter()


@images_router.post("/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
