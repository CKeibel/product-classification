from typing import Annotated

from fastapi import Depends, HTTPException, Request
from qdrant_client import AsyncQdrantClient
from src.embedding_service import EmbeddingService
from transformers import PreTrainedModel, ProcessorMixin


def get_embedding_model(request: Request) -> PreTrainedModel:
    model = getattr(request.app.state, "model", None)
    if not model:
        raise HTTPException(
            status_code=500, detail="Embedding model dependency not found!"
        )
    return model


def get_processor(request: Request) -> ProcessorMixin:
    processor = getattr(request.app.state, "processor", None)
    if not processor:
        raise HTTPException(status_code=500, detail="Processor dependency not found!")
    return processor


def get_qdrant_client(request: Request) -> AsyncQdrantClient:
    client = getattr(request.app.state, "qdrant_client", None)
    if not client:
        raise HTTPException(
            status_code=500, detail="Qdrant database connection is unavailable."
        )
    return client


EmbeddingModelDep = Annotated[PreTrainedModel, Depends(get_embedding_model)]
ProcessorDep = Annotated[ProcessorMixin, Depends(get_processor)]
QdrantDep = Annotated[AsyncQdrantClient, Depends(get_qdrant_client)]


def get_embedding_service(
    model: EmbeddingModelDep, processor: ProcessorDep
) -> EmbeddingService:
    return EmbeddingService(model=model, processor=processor)


EmbeddingServiceDep = Annotated[EmbeddingService, Depends(get_embedding_service)]
