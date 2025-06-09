# Flask API с PostgreSQL
Структура проекта:
```
app/
__init__.py
models.py
routes.py
requirements.txt
Dockerfile
docker-compose.yml
.env
Jenkinsfile
README.md
```
## Требуется установленные: Docker, Docker Compose, Git

Клонируем репозиторий, переходим в папку с проектом, вводим команду:
```
docker compose up --build
```
Должны подняться контейнеры с приложением и базой данных Postgresql.
На этапе сборки может не создаться таблица в бд, необходимо пофиксить:
```
docker-compose run web flask shell

#в shell создадим таблицу
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```
После запускаем и все должно отработать. С помощью curl проверяем работу:
```
curl -X POST http://localhost:5000/submit \
-H "Content-Type: application/json" \
-d '{"name": "Kirill", "score": 88}'

curl http://localhost:5000/ping

curl http://localhost:5000/results
```

## Jenkins
Checkout
- Клонирует репозиторий с использованием SSH-ключей
- Использует учетные данные GitHub (github-credentials)

Build
- Собирает Docker-образ
- Использует переменные окружения для имени образа

Test/Lint
- Запускает параллельно две задачи:
- Lint: проверка кода с помощью flake8
- Test: запуск тестов с помощью pytest
- Обе задачи выполняются внутри Docker-контейнера

Push
- Авторизуется в Docker Registry
- Отправляет собранный образ в registry
- Использует учетные данные registry (docker-registry-credentials)

Deploy
- Использует SSH для подключения к удаленной машине
- Создает необходимые директории
- Копирует необходимые файлы (docker-compose.yml, .env)
- Создает и копирует скрипт развертывания
- Выполняет развертывание на удаленной машине
- Использует учетные данные SSH (deploy-ssh-key)

Для работы этого pipeline нужно настроить в Jenkins следующие учетные данные:
- GitHub credentials (github-credentials):
- Тип: SSH Username with private key
- ID: github-credentials
- Username: ваш GitHub username
- Private Key: ваш SSH-ключ для GitHub

Docker Registry credentials (docker-registry-credentials):
- Тип: Username with password
- ID: docker-registry-credentials
- Username: ваш логин в Docker Registry
- Password: ваш пароль/токен для Docker Registry

Deploy SSH credentials (deploy-ssh-key):
- Тип: SSH Username with private key
- ID: deploy-ssh-key
- Username: пользователь для деплоя
- Private Key: SSH-ключ для доступа к серверу

## ENDPOINT
http://37.9.53.26:5000/result
