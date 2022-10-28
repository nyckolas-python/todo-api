# todo-api
with Django, DRF, Postgres, Celery + Redis, Docker

# How to run a project on your local machine?
1. Install Docker https://docs.docker.com/engine/install/
1.1. Please check and specify docker-compose.yml environment variables.
2. Run `docker-compose up --build pgadmin`
3. If you have [Errno 13] Permission denied: '/var/lib/pgadmin/sessions'
use command to give permissions `sudo chmod -R 777 ./pgadmin`
4. Open http://localhost:5050/browser/ add connect to server with:
`DB_HOST: postgres`
`POSTGRES_DB: todo_api_dev`
`POSTGRES_USER: todo_api_dev`
`POSTGRES_PASSWORD: pass`
5. Run `docker-compose up --build`
6. If you have error /data/db: permission denied failed to solve run: `sudo chmod -R 777 ./data/db`
7. Run migrations by `docker exec -it todo_api_web python manage.py migrate`
8. Run to create admin user `docker exec -it todo_api_web python manage.py createsuperuser` 
9. Open http://localhost:8080/admin/ in browser and auth with user created at step 8
10. Open http://127.0.0.1:8080/api/v1/task/ in browser login and create First task
11. Open http://127.0.0.1:8080/swagger/ in browser to see swagger documentation
