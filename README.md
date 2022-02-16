# django

## Установка и запуск проекта

- `python3 -m venv .venv` - создать виртуальное окружение
- `.venv/bin/activate.bat` - активировать виртуальное окружение
- `pip install -r requirements.txt` - установить зависимости
- Подключить базу данных PostgresQL (Создать пользователя согласно данным в settings.py)
- `python manage.py migrate` - применить миграции к базе данных
- `python manage.py runserver` - запуск сервера для разработки 