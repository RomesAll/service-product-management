from fastapi import FastAPI
from core import settings
from app.repositories.products import *
import uvicorn

app = FastAPI()

@app.get("/health-check")
def health_check():
    settings.logger.info("Health check")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)