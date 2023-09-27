# Django Backend Neobank

## Deploying your local environment using docker simulating the QA and Prod deployment

### pre requirements

- Install Docker
  - on linux run the following command: ```sudo apt install docker docker-compose```
    - to use docker without sudo read the following link: https://docs.docker.com/engine/install/linux-postinstall/
  - on windows download docker desktop from: https://docs.docker.com/desktop/windows/install/
  - on mac download docker desktop from: https://docs.docker.com/desktop/mac/install/
  - to avoid IP’s conflicts between your docker subnet and your VPN follow this link: https://portalfinance.atlassian.net/wiki/spaces/TDD/pages/2065956962
- create an environment file with the following command: ```cp .env.example .env.local```
  - change the database config if you need use a database different at docker compose file


### Running your environment

- run a postgres container from docker-compose: 
```shell
make neobank-services-up
```
- or use
```shell
docker-compose -f docker-compose.yml up db
```

- if it is the first time you run the django project locally you may want to run the project and build the database from your local host

- at this point your environment is almost ready run the following command to set your app running: 
  - first build your app image with: 
  ```shell
  make neobank-build
  ``` 
  
  **or run** 
  
  ```shell
  docker-compose -f docker-compose.yml build django
  ```
  - then run the container set with: 
  ```shell
  make neobank-up
  ``` 
  
  **or run** 
  
  ```shell
  docker-compose -f docker-compose.yml up django
  ```

## Use project locally

### Build docker Image

 - run: `docker-compose -f docker-compose.yml build django`

### Run django app

  - run: `make neobank-up`

  ### Run tests
  - You  need postgres running, run: `make neobank-tests`


## API documentation

### Swagger url:
  - You  need make collectstatic, run: `make neobank-collectstatic`
  - http://localhost:8000/v1/swagger/#
