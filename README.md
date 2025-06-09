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


