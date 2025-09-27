from fastapi import UploadFile
from fastapi import APIRouter
import base64
from app.schema.images import (
    ImageResize,
    ImageScale,
    FilterEnum,
)
import os
from pathlib import Path
from app.temp.images import apply_filter, lossy_resize, scale_image
from fastapi.responses import StreamingResponse
import io
from file_flow_common import db
from file_flow_common.schema.query import DbAccessQuery
from app.celery_client import celery_app
from app.utils.context import Context


images_router = APIRouter()


def get_streaming_response(image) -> StreamingResponse:
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/jpeg")


@images_router.post("/")
async def create_upload_file(file: UploadFile):
    content = await file.read()

    b64_img = base64.b64encode(content).decode("utf-8")
    ctx = Context()

    id = db.insert_document(
        db_query=DbAccessQuery(
            mongo_uri=ctx.MONGO_URI,
            db_name=ctx.DB_NAME,
            collection_name="images",
        ),
        data={"base64": b64_img},
    )
    return {"id": id}


@images_router.post("/lossy-resize/{id}/width/{width}/height/{height}")
async def resize_image(image_resize: ImageResize):
    filtered_image = lossy_resize(
        image_path=id,
        width=image_resize.width,
        height=image_resize.height,
    )

    return get_streaming_response(filtered_image)


@images_router.post("/scale/{id}/factor/{factor}")
async def scale_by_factor_image(image_scale: ImageScale):
    filtered_image = scale_image(
        image_path=id,
        percent=image_scale.factor,
    )

    return get_streaming_response(filtered_image)


@images_router.post("/{id}/all-filter-stack")
async def get_all_filtered_images(id: str):
    results = {}
    for f in FilterEnum:
        image = apply_filter(id, f.value)
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        results[f.value] = base64.b64encode(buf.getvalue()).decode("utf-8")

    return results


@images_router.delete("/purge-images-older-than-{days}-days")
async def purge_images_older_than_days(days: int):
    return {
        "deletedCount": db.delete_documents_older_than_ts(
            collection="images", days=days
        )
    }


@images_router.get("/{id}/apply-filter/{filter_name}")
async def apply_filter(id: str, filter_name: FilterEnum):
    task = celery_app.send_task(
        "apply_filter",
        args=[id, filter_name.value],
        queue="images",
    )
    result = task.get(timeout=30)
    if "image_b64" not in result:
        raise ValueError("Response incomplete")
    return {"result": result["image_b64"]}
