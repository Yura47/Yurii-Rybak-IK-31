# **Лабораторна робота №4**
---
## Послідовність виконання лабораторної роботи:
#### 1. Для ознайомляння з `Docker` звернувся до документації.
#### 2. Для перевірки чи докер встановлений і працює правильно на віртуальній машині запустітив перевірку версії командою `sudo docker -v > my_work.log`, виведення допомоги командою `sudo docker --help >> my_work.log` та тестовий імедж командою `sudo docker run docker/whalesay cowsay Docker is fun >> my_work.log`. Вивід цих команд перенаправляв у файл `my_work.log` та закомітив його до репозиторію.
#### 3. `Docker` працює з Імеджами та Контейнерами. Імедж це свого роду операційна система з попередньо інстальованим ПЗ. Контейнер це запущений Імедж. Ідея роботи `Docker` дещо схожа на віртуальні машини. Спочатку створив імедж з якого буде запускатись контейнер.
#### 4. Для знайомства з `Docker` створив імедж із `Django` сайтом зробленим у попередній роботі.
1. ##### Оскільки мій проект на `Python` то і базовий імедж також потрібно вибрати відповідний. Використовую команду `docker pull python:3.8-slim` щоб завантажити базовий імедж з репозиторію. Переглядаю створеного вміст імеджа командою `docker inspect python:3.8-slim`
    ##### Перевіряю чи добре встановився даний імедж командою:
    
```text
~/tpis/Yurii-Rybak-IK-31/lab_4$ sudo docker images
REPOSITORY        TAG        IMAGE ID       CREATED       SIZE
python            3.8-slim   1e46b5746c7c   2 days ago    122MB
docker/whalesay   latest     6b362a9f73eb   6 years ago   247MB 
```
2. ##### Створив файл з іменем `Dockerfile` та скопіював туди вміс такого ж файлу з репозиторію викладача.
    ###### Вміст файлу `Dockerfile`:
```text
    FROM python:3.8-slim
    
    LABEL author="Bohdan"
    LABEL version=1.0
    
    # оновлюємо систему
    RUN apt-get update && apt-get upgrade -y
    
    # Встановлюємо потрібні пакети
    RUN apt-get install git -y && pip install pipenv
    
    # Створюємо робочу папку
    WORKDIR /lab
    
    # Завантажуємо файли з Git
    RUN git clone https://github.com/BobasB/devops_course.git
    
    # Створюємо остаточну робочу папку з Веб-сайтом та копіюємо туди файли
    WORKDIR /app
    RUN cp -r /lab/devops_course/lab3/* .
    
    # Інсталюємо всі залежності
    RUN pipenv install
    
    # Відкриваємо порт 8000 на зовні
    EXPOSE 8000
    
    # Це команда яка виконається при створенні контейнера
    ENTRYPOINT ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
```
3. ##### Ознайомився із коментарями та зрозумів структуру написання `Dockerfile`.
4. ##### Змінений`Dockerfile` файл:
```text
FROM python:3.8-slim

LABEL author="Yura"
LABEL version=1.0

# оновлюємо систему
RUN apt-get update && apt-get upgrade -y

# Встановлюємо потрібні пакети
RUN apt-get install git -y && pip install pipenv

# Створюємо робочу папку
WORKDIR /lab

# Завантажуємо файли з Git
RUN git clone https://github.com/Yura47/Yurii-Rybak-IK-31.git

# Створюємо остаточну робочу папку з Веб-сайтом та копіюємо туди файли
WORKDIR /app
RUN cp -r /lab/Yurii-Rybak-IK-31/lab_3/* .

# Інсталюємо всі залежності
RUN pipenv install

# Відкриваємо порт 8000 на зовні
EXPOSE 8000

# Це команда яка виконається при створенні контейнера
ENTRYPOINT ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
```
#### 5. Створив власний репозиторій на Docker Hub. Для цього залогінився у власний аккаунт на `Docker Hub` після чого перейшов у вкладку Repositories і далі натиснув кнопку `Create new repository`.
#### 6. Виконав білд (build) Docker імеджа та завантажтажив його до репозиторію. Для цього я повинен вказати правильну назву репозиторію та TAG. Оскільки мій репозиторій rybakyurii/lab_4 то команда буде виглядати sudo docker build -t rybakyurii/lab_4:django ., де django - це тег.
Команда `docker images`:
```text
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_4$ sudo docker images
REPOSITORY         TAG        IMAGE ID       CREATED          SIZE
rybakyurii/lab_4   django     1a37bdd7a9b5   10 minutes ago   331MB
python             3.8-slim   1e46b5746c7c   2 days ago       122MB
docker/whalesay    latest     6b362a9f73eb   6 years ago      247MB
```
Команда для завантаження на власний репозеторій `sudo docker push rybakyurii/lab_4:django`.
Посилання на мій [`Docker Hub`](https://hub.docker.com/repository/docker/rybakyurii/lab_4) репозиторій та посилання на [`імедж`](https://hub.docker.com/layers/180733558/rybakyurii/lab_4/django/images/sha256-4274cffbbee6eac8299d18fcbfbb7e5dc584d17ccc9f64f10452d453cd1e0804?context=repo).
#### 7. Для запуску веб-сайту виконав команду `sudo docker run -it --name=django --rm -p 8000:8000 rybakyurii/lab_4:django`:
```text
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_4$ sudo docker run -it --name=django --rm -p 8000:8000 rybakyurii/lab_4:django
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
December 05, 2021 - 10:54:05
Django version 3.2.9, using settings 'my_site.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
[05/Dec/2021 10:56:10] "GET / HTTP/1.1" 200 167
Not Found: /favicon.ico
[05/Dec/2021 10:56:11] "GET /favicon.ico HTTP/1.1" 404 2440
```
Перейшов на адресу http://127.0.0.1:8000 та переконався що мій веб-сайт працює
#### 8. Оскільки веб-сайт готовий і працює, потрібно створит ще один контейнер із програмою моніторингу нашого веб-сайту (Моє Завдання на роботу):
1. ##### Створив ще один Dockerfile з назвою `Dockerfile.site` в якому помістив програму моніторингу.
    Вміст файлу `Dockerfile.site`:
```
FROM python:3.8-slim

LABEL author="Yura"
LABEL version=1.0

# оновлюємо систему
RUN apt-get update && apt-get upgrade -y

# Встановлюємо потрібні пакети
RUN apt-get install git -y && pip install pipenv

# Створюємо робочу папку
WORKDIR /lab

# Завантажуємо файли з Git
RUN git clone https://github.com/Yura47/Yurii-Rybak-IK-31.git

# Створюємо остаточну робочу папку з Веб-сайтом та копіюємо туди файли
WORKDIR /app
RUN cp -r /lab/Yurii-Rybak-IK-31/lab_3/* .

# Інсталюємо всі залежності
RUN pipenv install

# Відкриваємо порт 8000 на зовні
EXPOSE 8000

# Це команда яка виконається при створенні контейнера
ENTRYPOINT ["pipenv", "run", "python", "monitoring.py", "0.0.0.0:8000"]
```
2. ##### Виконав білд даного імеджа та дав йому тег `monitoring` командами:
    ```text
    sudo docker build -f Dockerfile.site -t rybakyurii/lab_4:monitoring .
    docker push rybakyurii/lab_4:monitoring
    ```
3. ##### Запустив два контейнери одночасно (у різних вкладках) та переконався що програма моніторингу успішно доступається до сторінок мого веб-сайту.
    ##### Використовуючи команди:
    Запуск серевера:
```text
    rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_4$ sudo  docker run -it --name=django --rm -p 8000:8000 rybakyurii/lab_4:django
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
December 05, 2021 - 11:10:01
Django version 3.2.9, using settings 'my_site.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
[05/Dec/2021 11:13:31] "GET /health HTTP/1.1" 301 0
[05/Dec/2021 11:13:31] "GET /health/ HTTP/1.1" 200 340
[05/Dec/2021 11:14:31] "GET /health HTTP/1.1" 301 0
[05/Dec/2021 11:14:31] "GET /health/ HTTP/1.1" 200 340
```
    Запуск моніторингу:
```text
sudo docker run -it --name=monitoring --rm --net=host -v $(pwd)/server.log:/app/server.log rybakyurii/lab_4:monitoring
    ^CTraceback (most recent call last):
      File "monitoring.py", line 32, in <module>
        time.sleep(60)
    KeyboardInterrupt
```
    (перед запуском моніторингу спочатку створив файл server.log)
    Вміст файла `Server.log`:
```text
INFO 2021-12-05 11:13:31,242 root : Сервер доступний. Час на сервері: Time: 11:13:31   Data: 2021/13/12/05/21
INFO 2021-12-05 11:13:31,242 root : Запитувана сторінка: : localhost:8000/health/
INFO 2021-12-05 11:13:31,243 root : Відповідь сервера місти наступні поля:
INFO 2021-12-05 11:13:31,243 root : Ключ: date, Значення: Time: 11:13:31   Data: 2021/13/12/05/21
INFO 2021-12-05 11:13:31,243 root : Ключ: current_page, Значення: localhost:8000/health/
INFO 2021-12-05 11:13:31,243 root : Ключ: server_info, Значення: Name_OS: Linux;   Name_Node: 7b3e6ef4ece5;   Release: 5.11.0-40-generic;   Version: #44~20.04.2-Ubuntu SMP Tue Oct 26 18:07:44 UTC 2021;   Indentificator:x86_64
INFO 2021-12-05 11:13:31,243 root : Ключ: client_info, Значення: Browser: python-requests/2.26.0;   IP: 172.17.0.1
INFO 2021-12-05 11:14:31,318 root : Сервер доступний. Час на сервері: Time: 11:14:31   Data: 2021/14/12/05/21
INFO 2021-12-05 11:14:31,319 root : Запитувана сторінка: : localhost:8000/health/
INFO 2021-12-05 11:14:31,319 root : Відповідь сервера місти наступні поля:
INFO 2021-12-05 11:14:31,319 root : Ключ: date, Значення: Time: 11:14:31   Data: 2021/14/12/05/21
INFO 2021-12-05 11:14:31,319 root : Ключ: current_page, Значення: localhost:8000/health/
INFO 2021-12-05 11:14:31,319 root : Ключ: server_info, Значення: Name_OS: Linux;   Name_Node: 7b3e6ef4ece5;   Release: 5.11.0-40-generic;   Version: #44~20.04.2-Ubuntu SMP Tue Oct 26 18:07:44 UTC 2021;   Indentificator:x86_64
INFO 2021-12-05 11:14:31,319 root : Ключ: client_info, Значення: Browser: python-requests/2.26.0;   IP: 172.17.0.1
```
4. ##### Закомітив `Dockerfile.site` та результати роботи програми моніторингу запущеної з `Docker` контейнера.
