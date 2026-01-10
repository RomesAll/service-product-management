from fastapi import FastAPI
from core import settings
from app.api.v1 import procurements_router, type_products_router, products_router
from app.core.exception_handlers import exception_handler
import uvicorn

app = FastAPI()
exception_handler(app)
app.include_router(products_router)
app.include_router(type_products_router)
app.include_router(procurements_router)

@app.get("/health-check")
def health_check():
    settings.logger.info("Health check")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)