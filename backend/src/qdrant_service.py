from qdrant_client import AsyncQdrantClient


class QdrantService:
    def __init__(self, client: AsyncQdrantClient) -> None:
        self.client = client

    async def search(self, embedding: list[float]) -> list[str]:
        pass
