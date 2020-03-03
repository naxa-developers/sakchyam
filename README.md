# sakchyam
Sakchyam data visualization web application


[![CircleCI](https://circleci.com/gh/naxa-developers/sakchyam/tree/master.svg?style=svg)](https://circleci.com/gh/naxa-developers/sakchyam/tree/master) [![Maintainability](https://api.codeclimate.com/v1/badges/a89b6658ac3885befb78/maintainability)](https://codeclimate.com/github/naxa-developers/sakchyam/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/a89b6658ac3885befb78/test_coverage)](https://codeclimate.com/github/naxa-developers/sakchyam/test_coverage)



### Steps To Follow

- Clone this repository

- Install docker and docker-compose in your system.
 Docker Refrence [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
 
- Create docker-compose.yml file

- Rename .env_sample to .env and change it settings accordingly for the project

- Inside dvs folder rename local_settings_sample.py to local_settings.py and change it settings accordingly for the project

- Bulid docker image
```sh
   docker-compose build
 ```

- Run external services
```sh
   docker-compose -f external_services.yml up -d
 ```

- Run the project in docker
```sh
   docker-compose up -d
 ```

>Note:
> for logs run docker-compose logs -f --tail 100
>check docker container status docker ps / docker ps -a
