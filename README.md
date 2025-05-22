# Сервис для улучшения качества изображения

В данном проекте реализован сервис для улучшения качества изображения с помощью
DL-моделей. В нем можно повысить разрешение изображения, убрать с изображения
смазы и шумы. Для повышения разрешения используется модель Real-ESRGAN, для
удаления смазов модель MLWNet, а для удаления шумов SCUNet.

## Структура репозитория

```
├───src
│   ├───models  # модели
│   │   │
│   │   ├───mlwnet
│   │   │   ├───local_arch.py
│   │   │   ├───MLWNet_arch.py
│   │   │   └───wavelet_block.py
│   │   │
│   │   ├───real_esrgan
│   │   │   └───generator.py
│   │   │
│   │   ├───scunet
│   │   │   └───model.py
│   │   │
│   │   ├───weights
│   │   │   └───README.md
│   │   │
│   │   ├───image_enhance.py  # класс для улучшения изображений
│   │   ├───model_configs.yaml  # конфиги моделей
│   │   └───worker.py   # обработчик изображений
│   │
│   └───services  # сервис
│       │
│       ├───fastapi_app  # API-сервис
│       │   │
│       │   ├───predict
│       │   │   └───router.py
│       │   │
│       │   ├───telegram_bot  # telegram-бот
│       │   │   ├───bot.py
│       │   │   ├───handlers
│       │   │   │   ├───keyboards.py
│       │   │   │   └───predict_router.py
│       │   │   │
│       │   │   └───bot.py
│       │   │
│       │   ├───Dockerfile
│       │   ├───main.py
│       │   └───requirements.txt
│       │
│       └───streamlit_app  # streamlit-приложение
│           │
│           ├───examples
│           │   ├───ex_1.jp
│           │   ├───ex_2.jpg
│           │   └───ex_3.jpg
│           │
│           ├───Dockerfile
│           ├───enhance_page.py
│           ├───main.py
│           ├───requirements.txt
│           └───start_page.py
│
├───.env-example
├───.gitignore
├───.pre-commit-config.yaml
├───docker-compose.yml
├───Dockerfile
├───poetry.lock
├───pyproject.toml
├───README.md
└───requirements.txt
```

## Развертывание сервиса

Для того, чтобы развернуть сервис нужно выполнить следующие шаги:

1. Склонировать репозиторий:
   ```
   git clone https://github.com/vladparh/image_enhancement_app.git
   cd image_enhancement_app
   ```
2. Добавить веса моделей в директорию [weights](src/models/weights) и при необходимости поправить [model_configs.yaml](src/models/model_configs.yaml)
3. Заменить `.env-example` на `.env` с необходимыми параметрами окружения
   окружения:
   - TELEGRAM_BOT_TOKEN: токен для telegram-бота
   - WEBHOOK_BASE_SITE: url для вебхука для работы telegram-бота
   - RABBITMQ_DEFAULT_USER: пользователь для RabbitMQ
   - RABBITMQ_DEFAULT_PASS: пароль для RabbitMQ
   - POLLING_INTERVAL: пауза между опросами API-сервиса
   - API_TIMEOUT: время, в течение которого соединение открыто (параметр для long polling)
4. Выполнить команду:
   ```
   docker compose up
   ```
   Всё! Streamlit-приложение развернуто на порту 8501, API-сервис на порту 8000,
   информацию по RabbitMQ можно посмотреть на порту 15672.

## Добавление новых моделей

Чтобы добавить новую модель, нужно:

1. Добавить скрипт pytorch-модели в директорию [models](src/models)
2. Добавить конфигурацию модели в
   [model_configs.yaml](src/models/model_configs.yaml)
3. Добавить модель в метод `load_model` класса `Enhancer` в
   [image_enhance.py](src/models/image_enhance.py)
