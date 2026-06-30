from pydantic import BaseModel, ConfigDict


class Hit(BaseModel):
    id: str
    model_config = ConfigDict(extra="ignore")
    name: str
    score: float
    description: str
    image_path: str
