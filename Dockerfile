FROM python:3.12-alpine
WORKDIR /services
RUN pip install --upgrade pip
RUN apk add curl
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir "app" "test"
COPY /app ./app
COPY /test ./test
COPY /alembic.ini .
EXPOSE 8000
CMD ["python", "app/main.py"]