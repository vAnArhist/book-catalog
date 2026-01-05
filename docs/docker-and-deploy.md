# Docker і запуск проєкту

Цей розділ описує, як проєкт Book Catalog запускається,
працює та розгортається за допомогою Docker.

Docker використовується для:
- відтворюваного середовища
- простого запуску “однією командою”
- ізоляції залежностей (Python, PostgreSQL)

---

## Загальна схема
```
Браузер
↓
Django (container: backend)
↓
PostgreSQL (container: db)
```


Усі компоненти описані в `docker-compose.yml`.

---

## Компоненти Docker

### Backend (Django)

Контейнер `backend`:
- запускає Django-сервер
- містить бізнес-логіку
- працює з шаблонами та ORM

Основні технології:
- Python 3.12
- Django
- Gunicorn (для production)

---

### Database (PostgreSQL)

Контейнер `db`:
- PostgreSQL
- зберігає всі дані (книги, теги, автори)

Дані БД зберігаються у Docker volume, тому:
- вони не зникають після перезапуску
- безпечні при rebuild контейнерів

---

## Структура файлів

```
bookstore-jango/
├── docker-compose.yml
├── backend/
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── manage.py
│ ├── backend/
│ ├── catalog/
│ └── media/
```


---

## docker-compose.yml

Файл `docker-compose.yml` описує всі сервіси.

Основні сервіси:
- `backend` — Django
- `db` — PostgreSQL

Docker сам:
- створює мережу
- підʼєднує сервіси між собою
- керує запуском

---

## Dockerfile (backend)

`Dockerfile` описує:
- базовий Python-образ
- встановлення залежностей
- копіювання коду
- команду запуску

Важливо:
- залежності фіксуються в `requirements.txt`
- код проєкту копіюється в контейнер

---

## Змінні середовища

Проєкт використовує змінні середовища для конфігурації:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

Це дозволяє:
- не хардкодити конфігурацію
- мати різні налаштування для dev / prod

---

## Запуск проєкту (development)

### Перший запуск

```bash
docker compose up --build
```

Docker:

збирає образи
запускає PostgreSQL
запускає Django
застосовує міграції
стартує сервер

## Повторний запуск

```docker compose up```

## Запуск у фоні

```docker compose up -d```

## Міграції

Міграції виконуються автоматично при старті backend-контейнера.

Також можна запускати вручну:

```docker compose exec backend python manage.py migrate```

## Створення суперкористувача

```docker compose exec backend python manage.py createsuperuser```

## Media-файли (обкладинки, скани)

Media-файли зберігаються:

- у папці `backend/media`

- або у Docker volume (залежно від конфігурації)

Це дозволяє:

- не втрачати файли при перезапуску

- масштабувати систему згодом

