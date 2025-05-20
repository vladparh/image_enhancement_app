FROM python:3.10-slim

RUN mkdir /worker

WORKDIR /worker

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY /src/models ./src/models/

CMD ["python", "-m", "src.models.worker"]
