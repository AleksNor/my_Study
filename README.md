## Интернет магазин по продаже техники

Проект разработан на фреймворке Django. Обращение за данными происходит по API, который реализован с использованием Django Rest Framework.

В рамках проекта:
- Разработал Django-шаблоны
- Разработал базу данных MySQL через Django ORM
- Поработал с администативной панелью Django(Подключение своих моделей, фильтрация, сортировка записей и т.д.)
- Выполнял тестовые http запросы через Insomnia
- Применил авторизацию и аутентификацию пользователей
- Написал тесты для Veiw функций и классов
- Использовал Swager для создания документации
- Настраивал логи в проекте
- Настроил кэширование
- 

## Установка и запуск проекта
1. Клонировать репозиторий, создать и войти в виртуальное окружение
2. `pip install -r requirements.txt` - установка зависимостей
3. Создание бд:
`cd ../mysite && python manage.py make migrations` - создание миграций
`python manage.py migrate` - миграция
`python manage.py runserver` - запуск сервера
