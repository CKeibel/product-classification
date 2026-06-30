from PIL import Image
from transformers import PreTrainedModel, ProcessorMixin


class EmbeddingService:
    def __init__(self, model: PreTrainedModel, processor: ProcessorMixin) -> None:
        self.model = model
        self.processor = processor

    def embed(self, image: Image.Image) -> list[float]:
        return self.model.embed(
            **self.processor(image, text="<image>", return_tensors="pt").to(
                self.model.device
            )
        ).tolist()[0]
