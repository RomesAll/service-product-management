from fastapi import FastAPI, Request
from core import settings
from app.api.v1 import procurements_router, type_products_router, products_router, auth_router
from app.core.exception_handlers import exception_handler
from datetime import datetime, timezone
import uvicorn, time

app = FastAPI()
exception_handler(app)
app.include_router(products_router)
app.include_router(type_products_router)
app.include_router(procurements_router)
app.include_router(auth_router)

@app.middleware("http")
async def process_request(request: Request, call_next):
    time_start = time.time()
    response = await call_next(request)
    end_time = time.time() - time_start
    response.headers["X-Processing-Time-ms"] = str(end_time.__round__(4))
    response.headers['X-Date-Request'] = str(datetime.now(timezone.utc))
    return response

@app.get("/health-check")
def health_check():
    settings.logger.info("Health check")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)