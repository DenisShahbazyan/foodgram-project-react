![example workflow](https://github.com/DenisShahbazyan/foodgram-project-react/actions/workflows/main.yml/badge.svg)
### Описание: 

Дипломный проект "Продвинутый помошник" курса "Python-разработчик плюс" 

### Используемые технологии: 
- Python
- Django
- Django REST framework
- Nginx
- Docker
- Postgres
- Gunicorn

### Автор: 

<a href="https://github.com/DenisShahbazyan">Denis Shahbazyan</a><br>

### Установка 

Склонируйте проект на Ваш компьютер 
```sh 
git clone https://github.com/DenisShahbazyan/foodgram-project-react.git
``` 
Перейдите в папку с проектом 
```sh 
cd foodgram-project-react
``` 
Активируйте виртуальное окружение 
```sh 
python3 -m venv venv 
``` 
```sh 
source venv/bin/activate 
``` 

Обновите менеджер пакетов (pip) 
```sh 
pip3 install --upgrade pip 
``` 

Установите необходимые зависимости 
```sh 
pip3 install -r requirements.txt 
``` 
Готово! 

Запуск проекта.
```sh
python ./backend/foodgram/manage.py runserver
```



### Примеры: 

Примеры запросов можно посмотреть в документации после запуска проекта: 
Перейти в папку infra (из корня проекта)
```sh
cd infra
```
Выполнить команду 
```sh
docker-compose up
```
Проект запустится на адресе http://localhost, увидеть спецификацию API вы сможете по адресу http://localhost/api/docs/