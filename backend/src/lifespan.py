import sys
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import torch
from fastapi import FastAPI
from loguru import logger
from qdrant_client import AsyncQdrantClient
from src.settings import settings
from transformers import AutoModel, AutoProcessor


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any, Any]:

    try:
        if not torch.cuda.is_available():
            raise OSError("No cuda available!")

        model = (
            AutoModel.from_pretrained(
                settings.model_id, trust_remote_code=True, default_task="retrieval"
            )
            .eval()
            .to("cuda")
        )
        processor = AutoProcessor.from_pretrained(
            settings.model_id, trust_remote_code=True
        )
        app.state.model = model
        app.state.processor = processor

        qdrant_client = AsyncQdrantClient(url=settings.qdrant_url)

        await qdrant_client.get_collections()
        app.state.qdrant_client = qdrant_client

    except Exception as e:
        logger.error(f"An error occured during embedding model initialization: {e}")
        sys.exit(1)

    yield

    if hasattr(app.state, "qdrant_client"):
        await app.state.qdrant_client.close()
