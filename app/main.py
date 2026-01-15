from fastapi import FastAPI, Request, Response
from core import settings
from app.api.v1 import procurements_router, type_products_router, products_router, auth_router, users_router
from app.api.v2 import (procurements_router as procurements_router_v2,
                        products_router as products_router_v2)
from app.core.exception_handlers import exception_handler
from app.core.logging_config import *
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, time

app = FastAPI()
exception_handler(app)
app.include_router(products_router)
app.include_router(type_products_router)
app.include_router(procurements_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(procurements_router_v2)
app.include_router(products_router_v2)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def logging_request(request: Request, response: Response, time_processing):
    message = ("client: {0} url: {1} method: {2} status: {3} time: {4}"
               .format(request.client.host, request.url, request.method, response.status_code, time_processing))
    settings.logger_requests.info(message)

@app.middleware("http")
async def process_request(request: Request, call_next):
    time_start = time.time()
    response = await call_next(request)
    end_time = str((time.time() - time_start).__round__(4))
    response.headers["x-processing-time"] = end_time
    logging_request(request, response, end_time)
    return response

@app.get("/health-check")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)