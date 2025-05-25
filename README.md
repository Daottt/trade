### Зависимости
* Python 3.10
* Django 5.2
* Django REST framework 3.16
* PostgreSQL 16
### Запуск
Есть два способа запустить проект: используя Docker Compose или вручную.

### Docker Compose
1. Клонируем репозиторий
    ```bash
    git clone https://github.com/Daottt/trade.git
    cd trade
    ```
2. Запускаем контейнеры
    ```bash
    docker compose up
    ```
### Вручную
1. Устанавливаем зависимости
    ```bash
    pip install -r requirements.txt
    ```
2. Настраиваем подключение к базе данных. Создаём базу данных и прописываем переменные окружения:
    ``` bash
    DATABASE_NAME = "db_name"
    DATABASE_USERNAME = "name"
    DATABASE_PASSWORD = "password"
    ```
3. Применяем миграции
    ```bash
    python manage.py migrate
    ```
4. Создаём админа
    ```bash
    python manage.py initadmin
    ```
5. Запускаем сервер
    ```bash
    python manage.py runserver
    ```

### Тесты
Для запуска тестов
```bash
dotnet test
```

