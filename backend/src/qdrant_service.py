from qdrant_client import AsyncQdrantClient
from src.schemas import Hit


class QdrantService:
    def __init__(self, client: AsyncQdrantClient) -> None:
        self.client = client

    async def search(
        self, embedding: list[float], collection: str, limit: int
    ) -> list[Hit]:
        search_results = await self.client.query_points(
            query=embedding, limit=limit, with_payload=True, collection_name=collection
        )

        return [
            Hit(id=str(res.id), score=res.score, **(res.payload or {}))
            for res in search_results.points
        ]
