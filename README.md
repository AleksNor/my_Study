# Интернет магазин по продаже техники

Проект разработан на фреймворке Django. Обращение за данными происходит по API, который реализован с использованием Django Rest Framework.

# Установка и запуск проекта
1. Клонировать репозиторий, создать и войти в виртуальное окружение
2. `pip install -r requirements.txt` - установка зависимостей
3. Создание бд:
`cd ../mysite && python manage.py make migrations` - создание миграций
`python manage.py migrate` - миграция
`python manage.py runserver` - запуск сервера
