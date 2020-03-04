# Sakchyam Data Visaualization Web Application

![Imgur](https://i.imgur.com/h2ppROy.png) 

> Sakchyam Web Application
> For visaualization of Project
> Data and its services. 
> This project provides a way to 
> show the works sakchyam in a
> interactive way for user.





[![Requirements Status](https://requires.io/github/naxa-developers/sakchyam/requirements.svg?branch=master)](https://requires.io/github/naxa-developers/sakchyam/requirements/?branch=master) [![CircleCI](https://circleci.com/gh/naxa-developers/sakchyam/tree/master.svg?style=svg)](https://circleci.com/gh/naxa-developers/sakchyam/tree/master) [![Maintainability](https://api.codeclimate.com/v1/badges/a89b6658ac3885befb78/maintainability)](https://codeclimate.com/github/naxa-developers/sakchyam/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/a89b6658ac3885befb78/test_coverage)](https://codeclimate.com/github/naxa-developers/sakchyam/test_coverage) ![version](https://img.shields.io/badge/python-v3.6-orange?style=flat&logo=python)



## Installation

- Clone this repository

```sh
   git clone git@github.com:naxa-developers/sakchyam.git
 ```

- Install docker and docker-compose in your system. Docker Refrence Ubuntu

- Create a symlink with name docker-compose.yml to docker-compose.local.yml
```sh
   ln -s docker-compose.local.yml docker-compose.yml
 ```

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
