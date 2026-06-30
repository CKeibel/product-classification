from typing import Annotated

from fastapi import APIRouter, Depends
from PIL import Image
from src.dependencies import EmbeddingServiceDep, QdrantDep
from src.image_utils import parse_file

router = APIRouter()

ValidImageDep = Annotated[Image.Image, Depends(parse_file)]


@router.post("/embed-image")
async def create_image_embedding(
    image: ValidImageDep,
    embedding_service: EmbeddingServiceDep,
    qdrant_service: QdrantDep,
):

    vector = embedding_service.embed(image)
