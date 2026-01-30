# Deribit Price

Простой сервис для сбора и хранения индексных цен BTC и ETH с криптобиржи Deribit.  
Цены сохраняются каждую минуту в PostgreSQL.  
Предоставляется REST API на FastAPI для получения данных.

## Функционал

- Каждую минуту запрашивает `index_price` для BTC и ETH через Deribit API (использует `aiohttp`)
- Сохраняет: ticker (BTC/ETH), price (decimal), timestamp (unix)
- API (FastAPI):
  - `GET /prices?ticker=BTC` — все записи по тикеру
  - `GET /latest-price?ticker=ETH` — последняя цена
  - `GET /prices/filter?ticker=BTC&start_ts=...&end_ts=...` — цены за период

## Технологии

- Python 3.12
- FastAPI + Uvicorn
- SQLAlchemy 2.0 (async) + asyncpg
- Celery + Redis (для периодических задач)
- aiohttp (клиент Deribit)
- PostgreSQL
- Docker + docker-compose


## Design Decisions

- **Async** — весь стек асинхронный (FastAPI, SQLAlchemy async, aiohttp, Celery с asyncio.run)
- **Celery + Redis** — для надёжного периодического сбора данных (beat schedule каждые 60 сек)
- **Pydantic Settings** — безопасная загрузка конфига из .env
- **Decimal** для цены — точность хранения (избегаем float-ошибок)
- **Индексы** в БД на `ticker` и `ticker + timestamp` — быстрые запросы по тикеру и диапазону дат
- **Dependency Injection** (Depends) — чистая передача сессии в эндпоинты
- **Нет глобальных переменных** — всё через классы и DI
- **OOP** — отдельные классы для клиента, CRUD, настроек
- **Docker** — простое развёртывание (postgres + redis + app)

## Быстрый запуск (локально с Docker)

1. **Запустите все сервисы:**
    ```bash
    docker-compose up --build -d

2. **Создадутся контейнеры:**
 - postgres
 - redis
 - app (FastAPI)

3. **Запустите Celery worker (в отдельном терминале):**
    ```bash
    docker-compose exec app celery -A app.tasks.celery_app worker -l info

4. **Запустите Celery beat (в ещё одном терминале):**
    ```bash
    docker-compose exec app celery -A app.tasks.celery_app beat -l info

5. **Откройте документацию API:**
- `http://localhost:8000/docs`

6. **Примеры запросов:**
- `http://localhost:8000/latest-price?ticker=BTC`
- `http://localhost:8000/prices?ticker=ETH`
- `http://localhost:8000/prices/filter?ticker=BTC&start_ts=1735689600&end_ts=1735776000`
