# Архітектура системи

## Компоненти
- Django — бізнес-логіка
- PostgreSQL — зберігання даних
- Docker — ізольоване середовище
- HTML templates — UI

## Потік даних
Браузер → Django views → ORM → PostgreSQL → templates
