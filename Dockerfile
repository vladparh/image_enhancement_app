FROM python:3.10-slim

RUN mkdir /worker

WORKDIR /worker

COPY . .

RUN python -m pip install --no-cache-dir poetry==2.1.2 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-root \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

CMD ["python", "-m", "src.models.worker"]
