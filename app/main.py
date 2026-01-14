from fastapi import FastAPI, Request, Response
from core import settings
from app.api.v1 import procurements_router, type_products_router, products_router, auth_router, users_router
from app.core.exception_handlers import exception_handler
from app.core.logging_config import *
import uvicorn, time

app = FastAPI()
exception_handler(app)
app.include_router(products_router)
app.include_router(type_products_router)
app.include_router(procurements_router)
app.include_router(auth_router)
app.include_router(users_router)

def logging_request(request: Request, response: Response, time_processing):
    message = ("client: {0} url: {1} method: {2} status: {3} time: {4}"
               .format(request.client.host, request.url, request.method, response.status_code, time_processing))
    if request.url.path in ["/health-check", '/docs', '/favicon.ico', '/openapi.json']:
        settings.logger.debug(message)
    elif 100 <= response.status_code < 400:
        settings.logger.info(message)
    elif 400 <= response.status_code < 500:
        settings.logger.warning(message)
    elif 500 <= response.status_code < 600:
        settings.logger.error(message)

@app.middleware("http")
async def process_request(request: Request, call_next):
    time_start = time.time()
    response = await call_next(request)
    end_time = time.time() - time_start
    response.headers["x-processing-time"] = str(end_time.__round__(4))
    logging_request(request, response, end_time)
    return response

@app.post("/health-check")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)