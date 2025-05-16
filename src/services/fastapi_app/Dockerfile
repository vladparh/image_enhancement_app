FROM python:3.10-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
