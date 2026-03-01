# Department Management API

Тестовое задание в компанию hitalent
Ссылка на задание: https://docs.google.com/document/d/1MB0wtk2fC3uHOHwIuOOjk9az0gtyx2Xovmn-A0E7NBU/edit?tab=t.0#heading=h.sn3vl0z0iwpr

REST API для управления структурой подразделений и сотрудников компании. Позволяет создавать иерархическую структуру отделов, управлять сотрудниками и перемещать подразделения.

## Технологии

- **Python 3.14**
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy 2.0** - ORM для работы с БД
- **Alembic** - миграции базы данных
- **PostgreSQL** - база данных
- **Pydantic** - валидация данных
- **Docker** + **Docker Compose** - контейнеризация

## Установка и запуск

### Предварительные требования

- Установленные Docker и Docker Compose
- Или Python 3.14+ и PostgreSQL локально

### Запуск через Docker (рекомендуется)

1. **Клонировать репозиторий**
git clone <url-репозитория>
cd <имя-папки>

2. **Создать файл .env или отредактировать .env.example**

3. **Запустить контейнеры**
docker-compose up --build