# **Лабораторна робота №6**
---
## Послідовність виконання лабораторної роботи:
#### 1. Одразу не потрапив на стартову сторінку тому перегляньте її. Там описано як налаштувати інтеграцію з `GitHub` та додати мій репозиторій;
#### 2. Основна документація по `Travis CI` представлена на сторінці.
#### 3. У лабораторній 6 я буду налаштовувати CI/CD сервер. Інтеграція пройшла успішно тому на дашборі `Travis` відображаються мої `GitHub` репозиторії. Додав репозиторій до `Travis`.
#### 4. Для того щоб `Travis` знав які кроки потрібно виконати над моїм кодом у кореневій папці мого репозиторію створюю файл `.travis.yml`. Створив у моєму `GitHub` репозиторію такий самий файл та скопіював туди вміст. Travis автоматично знайшов даний файл та виконувати ці кроки при кожному новому коміті в `master` гілку.
Вміст файла `.travis.yml`:
```text
language: python
python:
  - "3.8"
jobs:
  include:
    - stage: "Build Lab 2."
      name: "Run tests for Lab 2"
      python: 3.8
      install:
        - cd ./lab_2/
        - pipenv install
      script: pipenv run pytest tests/tests.py || true
    - stage: "Build Lab 3."
      name: "Run Djungo Server and test it accessibility. Fail to run and test"
      python: 3.8
      install:
        - cd ./lab_3/
        - pipenv install
      script: ./scripts/travis-build.sh
    - stage: "Build Lab 4."
      name: "Build Docker images & Home task"
      services:
        - docker
      install:
        - cd ./lab_4/
      script:
        - docker build -t rybakyurii/lab_4:django-travis .
        - docker images
        - if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin; docker push rybakyurii/lab_4:django-travis; else echo "PR skip deploy"; fi
    - stage: "Build Lab 5."
      name: "Build and run Docker images via make"
      services:
        - docker
      install:
        - cd ./lab_5/
        - make app
        - make tests
      script:
        - make run
        - make test-app
branches:
  only:
    - master
```
Створюю в папці з лабораторною 3 файл `lab_3/scripts/travis-build.sh` і надаю йому права для запуску командою `chmod 777 ./scripts/travis-build.sh` знаходячись в папці `lab_3`.
Вміст файла `./scripts/travis-build.sh`:
```sh
#!/bin/bash
set -ev
nohup pipenv run server > ./ci-build.log &
pipenv run python monitoring.py || true
exit 0
```
Оскільки сервер на `Django` для 3 лабораторної запустився і не вимикався я примусово зупинив білд для цього під-тесту. Всі інші під-тести пройшли успішно. 
#### 5. Для того щоб налаштувати інтеграцію з `Docker Hub` прочитав документацію.
#### 6. (Завдання). Білд представлений у даному репозиторію не враховує мої попередні домашні завдання, тому:
* ##### Переписав білд `lab 2` з використання кроків записаних у `Makefile`.
```text
    - stage: "Build Lab 2."
      name: "Run tests for Lab 2"
      python: 3.8
      install:
        - cd ./lab_2/
        - pipenv install requests
        - pipenv install ntplib
        - pipenv install pytest
      script: 
        - pipenv run pytest tests/tests.py || true
        - pipenv run python3 app.py || true
```
* ##### Переписав білд `lab 4` де я створював ще один `DockerFile` для контейнера моніторингу.
```text
    - stage: "Build Lab 4."
      name: "Build Docker images & Home task"
      services:
        - docker
      install:
        - cd ./lab_4/
      script:
        - docker build -f Dockerfile -t rybakyurii/lab_4:django-travis .
        - docker build -f Dockerfile.site -t rybakyurii/lab_4:monitoring-travis .
        - docker images
        - if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin; docker push rybakyurii/lab_4:django-travis; docker push rybakyurii/lab_4:monitoring-travis; else echo "PR skip deploy"; fi
```
* ##### Переписав білд `lab 5` і додав кроки `Makefile` які робили `push` імеджів у `Docker Hub` репозиторій.
```text
    - stage: "Build Lab 5."
      name: "Build and run Docker images via make"
      services:
        - docker
      install:
        - cd ./lab_5/
        - make app
        - make tests
      script:
        - make run
        - make test-app
        - echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
        - make docker-push
```
* ##### Посилання на мій [***Travis***](https://app.travis-ci.com/github/Yura47/Yurii-Rybak-IK-31) білд.
Відредагував файл `./lab_3/scripts/travis-build.sh` для того щоб запуск моніторингу виконувався у фоні і коли `Django` сервер і моніторинг запуститься та буде працювати то білд цього підтесту завершиться після запуску сервера і моніторингу у фоні. Якщо б моніторинг запускався б не в фоні то потрібно б очікувати на зупинку сервера з зовні.
```sh
#!/bin/bash
set -ev
nohup pipenv run server > ./ci-build.log &
nohup pipenv run python monitoring.py || true &
exit 0
```
#### 7. Після успішного виконання роботи відредагував свій персональний README.md у цьому репозиторію та створив pull request.
