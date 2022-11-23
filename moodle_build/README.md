# Build Moodle for tesing
- Install docker and docker-compose
- Run the following commands for initial setup (only need to run these on first time)
```
docker volume create mariadb_data
docker volume create moodle_data
docker network create moodle-network
```
- Launch the website
```
docker-compose up -d
```
- Access the website at `http://<YOUR IP>:<HTTP_PORT>`. If you are running the site on localhost, either `http://localhost:<HTTP_PORT>` or `http://127.0.0.1:<HTTP_PORT>` works. `HTTP_PORT` is set in the `.env` file.

## Notes
- Read more about the environment variables of containers:
  - mariadb: https://hub.docker.com/r/bitnami/mariadb
  - moodle: https://hub.docker.com/r/bitnami/moodle
