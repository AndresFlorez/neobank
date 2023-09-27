# Django Backend Neobank

## Deploying your local environment using docker simulating the QA and Prod deployment

### pre requirements

- Install Docker
  - on linux run the following command: ```sudo apt install docker docker-compose```
    - to use docker without sudo read the following link: https://docs.docker.com/engine/install/linux-postinstall/
  - on windows download docker desktop from: https://docs.docker.com/desktop/windows/install/
  - on mac download docker desktop from: https://docs.docker.com/desktop/mac/install/
  - create an environment file with the following command: ```cp .env.example .env.local```
  - change the database config if you need use a database different at docker compose file


### Running your environment

- run a postgres container from docker-compose:
```shell
make neobank-services-up
```
- or use
```shell
docker-compose -f docker-compose.yml up -d db
```


- at this point your environment is almost ready run the following command to set your app running: 
  - first build your app image with: 
  ```shell
  make neobank-build
  ``` 
  **or run** 
  
  ```shell
  docker-compose -f docker-compose.yml build django
  ```
  - Create database tables, run makemigrations
  ```shell
  make neobank-migrate
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


## Overview
- As the project's foundation, I used the repository [Django-Styleguide-Example](https://github.com/HackSoftware/Django-Styleguide-Example/tree/master), which I obtained from Hacksoft's style guide, and removed everything I considered unnecessary.
- La configuración de Django (settings) se encuentra en config.django.base.
- For security, I used JSON Web Tokens (JWT). when creating a user or logging in, I add a token to the response cookies. It has an expiration time that can be configured with an environment variable (JWT_EXPIRATION_DELTA_SECONDS).
- All models stores Django model state on every create/update/delete.
- The applications are located in *neobank* folder, which are:
  - *api*
  - *authentication*
    - [POST] `/v1/auth/jwt/login/` user login.
    ```json
    {
      "email": "test0@test.com",
      "password": "DeV.2023"
    }
    ```
    - [POST] `/v1/auth/jwt/logout/` user logout.
  - *bank_accounts*
    - [POST] `/v1/bank_accounts/` create bank account.
    ```json
    {
      "account_number": "0123456789"
    }
    ```

    - [GET] `/v1/bank_accounts/` consult one or more bank accounts.
    - [POST] `/v1/bank_accounts/transactions/` create transactions (deposit and withdrawal) for a bank accounts.
    ```json
    {
      "bank_account": "{{bank_account}}",
      "transaction_type": "deposit",
      "amount": 1000000
    }
    ```

  - *common*
  - *users*
    - [POST] `/v1/users/` user registration.
     ```json
    {
      "email": "test0@test.com",
      "first_name": "Andres",
      "last_name": "Florez",
      "password": "DeV.2023",
      "user_profile": {
          "country": "colombia",
          "address": "calle 18a",
          "telephone": "+57 3104427917",
          "identification": "1144059543"
      }
    }
    ```
    - [GET] `/v1/users/me/` get logged user information.