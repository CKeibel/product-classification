import io

from fastapi import HTTPException, UploadFile
from PIL import Image


async def parse_file(file: UploadFile) -> Image.Image:

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="The uploaded file must be an image."
        )

    try:
        image_bytes = await file.read()

        image = Image.open(io.BytesIO(image_bytes))

        if image.mode != "RGB":
            image = image.convert("RGB")

        return image
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occured during file parsing: {e}"
        )
