![example workflow](https://github.com/DenisShahbazyan/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram

### Описание:
Дипломный проект "Продвинутый помошник" курса "Python-разработчик плюс". На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Развертывание:
#### Запуск веб-сервера::
- Склонируйте проект на Ваш компьютер 
```sh 
git clone https://github.com/DenisShahbazyan/foodgram-project-react.git
``` 
- Перейдите в папку с проектом 
```sh 
cd foodgram-project-react
``` 
- Создайте и активируйте виртуальное окружение 
```sh 
python -m venv venv 
source venv/Scripts/activate 
``` 
- Обновите менеджер пакетов (pip) 
```sh 
pip install --upgrade pip 
``` 
- Установите необходимые зависимости 
```sh 
pip install -r ./backend/requirements.txt
``` 
- Создайте базу данных `foodgram_postgres`
- Проверьте, что константа `IS_DOCKER` в файле `backend\foodgram\settings.py` == `False`
- Создайте миграции
```sh
python ./backend/manage.py makemigrations
python ./backend/manage.py migrate
```
- Заполните базу данных тестовыми данными
```sh
python ./backend/manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

cd backend/
python manage.py loaddata dump.json
cd ..
```
- Запуск сервера
```sh
python ./backend/manage.py runserver
```
- Сайт запуститься по адресу http://127.0.0.1:8000
- Спецификация API будет доступна http://127.0.0.1:8000/api/docs/

#### Запуск docker-контейнера:
- В папке `infra` создайте файл `.env` - в нем будут храниться переменные окружения для проекта. Пример его содержимого ниже:
```sh
SECRET_KEY=SECRET_KEY
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
PGADMIN_DEFAULT_EMAIL=admin@admin.ru
PGADMIN_DEFAULT_PASSWORD=admin
```
- Проверьте, что константа `IS_DOCKER` в файле `backend\foodgram\settings.py` == `True`
- Запуск docker-compose
```sh
cd infra/
docker-compose up -d
```
- Запустятся контейнеры, сайт будет доступен по адресу http://localhost/
- PgAdmin Будет доступен по адресу http://localhost:5050/
- Спецификация API будет доступна http://localhost/api/docs/

### Системные требования:
- [Python](https://www.python.org/) 3.10.4
- [PostgreSQL](https://www.postgresql.org/) 14
- [Pg Admin](https://www.pgadmin.org/) 4 
- [Docker](https://www.docker.com/) 4.10.1
- [Docker Compose](https://docs.docker.com/compose/) 3.9

### Планы по доработке:
>Я считаю что этот проект очень хорош в качестве учебного, и не планирую его дорабатывать.

### Используемые технологии:
- [Django](https://www.djangoproject.com/) 4.0.3
- [Django REST framework](https://www.django-rest-framework.org/) 3.13.1
- [DRF-EXTRA-FIELDS](https://pypi.org/project/django-extra-fields/) 3.0.2
- [django-filter](https://pypi.org/project/django-filter/) 21.1
- [djoser](https://djoser.readthedocs.io/en/latest/getting_started.html) 2.1.0
- [python-dotenv](https://pypi.org/project/python-dotenv/) 0.20.0
- [tqdm](https://pypi.org/project/tqdm/) 4.64.0

- [gunicorn](https://pypi.org/project/gunicorn/) 20.1.0
- [Nginx](https://nginx.org/ru/)

### Авторы:
- backend - [Denis Shahbazyan](https://github.com/DenisShahbazyan)
- frontend - [Yandex Praktikum](https://github.com/yandex-praktikum/foodgram-project-react)
