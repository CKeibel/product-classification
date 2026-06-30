from fastapi import FastAPI
from src.lifespan import lifespan
from src.router import router

app = FastAPI(lifespan=lifespan)
app.include_router(router)
