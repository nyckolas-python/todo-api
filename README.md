# todo-api
with Django, DRF, Postgres, Celery + Redis, Docker

# How to run a project on your local machine?
1. Install Docker https://docs.docker.com/engine/install/
2. Run `docker-compose up --build pgadmin`
If you have [Errno 13] Permission denied: '/var/lib/pgadmin/sessions'
use command to give permissions 'sudo chmod -R 777 ./pgadmin'
3. Open http://localhost:5050/browser/ add connect to server with:
'DB_HOST: postgres'
'POSTGRES_DB: todo_api_dev'
'POSTGRES_USER: todo_api_dev'
'POSTGRES_PASSWORD: pass'
4. Run `docker-compose up --build`
If you have error /data/db: permission denied failed to solve run: `sudo chmod -R 777 ./data/db`
5. Run migrations by `docker exec -it todo_api_web python manage.py migrate`
6. Run to create admin user `docker exec -it todo_api_web python manage.py createsuperuser` 
7. Open http://localhost:8080/admin/ in browser and auth with user created at step 9
