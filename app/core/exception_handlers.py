from sqlalchemy.exc import DBAPIError, DataError, IntegrityError, DatabaseError
from psycopg.errors import UniqueViolation
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .config import settings

def exception_handler(app: FastAPI):

    @app.exception_handler(DataError)
    def data_error_handler(request: Request, exception: DataError) -> JSONResponse:
        settings.logger.error("client: %s received an error: code: %s,  args: %s, "
                              "params: %s, statement: %s, detail: %s", request.client.host,
                              exception.code, exception.args, exception.params, exception.statement, exception.detail)
        return JSONResponse(status_code=500, content={'message': 'Server error'})

    @app.exception_handler(DBAPIError)
    def db_api_error_handler(request: Request, exception: DBAPIError) -> JSONResponse:
        settings.logger.error("client: %s received an error: code: %s,  args: %s, "
                              "params: %s, statement: %s, detail: %s", request.client.host,
                              exception.code, exception.args, exception.params, exception.statement, exception.detail)
        return JSONResponse(status_code=500, content={'message': 'Server error'})

    @app.exception_handler(IntegrityError)
    def integrity_error_handler(request: Request, exception: IntegrityError) -> JSONResponse:
        settings.logger.error("client: %s received an error: code: %s,  args: %s, "
                              "params: %s, statement: %s, detail: %s", request.client.host,
                              exception.code, exception.args, exception.params, exception.statement, exception.detail)
        error = exception.args[0]
        if error.find('UniqueViolation') != -1:
            message = error[error.find('DETAIL'):]
            return JSONResponse(status_code=412, content={'message': message})
        return JSONResponse(status_code=500, content={'message': 'Server error'})

    @app.exception_handler(DatabaseError)
    def data_base_error_handler(request: Request, exception: DatabaseError) -> JSONResponse:
        settings.logger.error("client: %s received an error: code: %s,  args: %s, "
                              "params: %s, statement: %s, detail: %s", request.client.host,
                              exception.code, exception.args, exception.params, exception.statement, exception.detail)
        return JSONResponse(status_code=500, content={'message': 'Server error'})

    @app.exception_handler(Exception)
    def indefinite_error_handler(request: Request, exception: Exception) -> JSONResponse:
        settings.logger.error("client: %s received an error: %s", request.client.host, exception)
        return JSONResponse(status_code=500, content={'message': 'Server error'})

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:
        if int(exception.status_code) >= 500:
            settings.logger.error("client: %s received an error: status: %s, detail: %s",
                                 request.client.host, exception.status_code, exception.detail)
            return JSONResponse(status_code=exception.status_code, content={'message': 'Server error'})
        settings.logger.warning("client: %s received an error: status: %s, detail: %s",
                              request.client.host, exception.status_code, exception.detail)
        return JSONResponse(status_code=exception.status_code, content={'message': exception.detail})