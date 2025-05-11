FROM python:3.10-slim

RUN mkdir /image_enhancement_app

WORKDIR /image_enhancement_app

COPY . .

RUN python -m pip install --no-cache-dir poetry==2.1.2 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-root \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

EXPOSE 8000

CMD ["uvicorn", "src.services.fastapi.main:app", "--host=0.0.0.0", "--port=8000"]