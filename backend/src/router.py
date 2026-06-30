from typing import Annotated

from fastapi import APIRouter, Depends, Form
from PIL import Image
from src.dependencies import EmbeddingServiceDep, QdrantServiceDep
from src.image_utils import parse_file
from src.schemas import Hit
from src.settings import settings

router = APIRouter()

ValidImageDep = Annotated[Image.Image, Depends(parse_file)]


@router.post("/embed-image", response_model=list[Hit])
async def create_image_embedding(
    image: ValidImageDep,
    embedding_service: EmbeddingServiceDep,
    qdrant_service: QdrantServiceDep,
    limit: int = Form(5, ge=1, le=50),
) -> list[Hit]:

    vector = embedding_service.embed(image)
    return await qdrant_service.search(vector, settings.collection_name, limit)
