# Re-creating Moodle build
## Instructions
- Install docker and docker-compose
- Run the following commands for initial setup (only need to run these on first time)
```
docker volume create mariadb_data
docker volume create moodle_data
docker volume create moodle
docker network create moodle-network
```
- For a fresh start, run the following command. If you want to reuse containers from previous run, skip this step
```
docker container prune
```
- Launch the website
```
docker-compose up -d
```
- Access the website
- Access the website at `http://<YOUR IP>:<HTTP_PORT>`. If you are running the site on localhost, either `http://localhost:<HTTP_PORT>` or `http://127.0.0.1:<HTTP_PORT>` works. `HTTP_PORT` is set in the `.env` file.

## Notes
- Template for `.env` file is available at `moodle_build/.env.example`
- Read more about the environment variables of containers:
  - mariadb: https://hub.docker.com/r/bitnami/mariadb
  - moodle: https://hub.docker.com/r/bitnami/moodle
- Data persists from run to run. In order to wipe out data from previous runs, delete and recreate three volumes: `moodle`, `moodel_data`, `mariadb_data`.
