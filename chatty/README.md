# Chatty
Chatty, the great communicator of our logic.

### Initializing the database
1. After you start Docker on your machine, cd into `chatty` and run `docker-compose up -d`, which should run the docker postgres db.
2. Verify the docker process is running by running `docker-compose ps`. The process will here on be referred to as {{YOUR_DOCKER_PROCESS}}
3. To verify the chatty database was created, run `docker exec -it {{YOUR_DOCKER_PROCESS}} psql -U postgres -c "\l"`. The chatty db should in the list.
---
**NOTE**:
If the db is not created, you should run:
```
$ docker exec -it {{YOUR_DOCKER_PROCESS}} psql -U postgres -c "CREATE DATABASE chatty;"
```
---
4. Next add a database user with username pg_user and password "password" by running
```
$ docker exec -it {{YOUR_DOCKER_PROCESS}} psql -U postgres -c "CREATE USER pg_user SUPERUSER PASSWORD 'password';"
$ docker exec -it {{YOUR_DOCKER_PROCESS}} psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE chatty TO pg_user;"
```
5. Install libpq with (assuming a zsh is being used)
```
$ brew install libpq
$ echo 'export PATH="/usr/local/opt/libpq/bin:$PATH"' >> ~/.zshrc
```
6. Migrate the db with `python manage.py migrate`.
7. Next create a superuser which will allow access to django's admin portal. Use the same username/password combo as the database (pg_user/password).
```
$ python manage.py createsuperuser
(Then follow the onscreen instructions)
```

Happy coding!
