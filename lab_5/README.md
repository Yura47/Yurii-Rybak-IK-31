# **Лабораторна робота №5**
---
## Послідовність виконання лабораторної роботи:
#### 1. Для ознайомляння з `docker-compose` звернувся до документації.
Щоб встановити `docker-compose` використав команди:
```text
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
#### 2. Ознайомився з бібліотекою `Flask`, яку найчастіше використовують для створення простих веб-сайтів на Python.
#### 3. Моє завдання: за допомогою Docker автоматизувати розгортання веб сайту з усіма супутніми процесами. Зроблю я це двома методами: 
* за допомогою `Makefile`;
* за допомогою `docker-compose.yaml`.

#### 4. Першим розгляну метод з `Makefile`, але спочатку створю робочий проект.
#### 5. Створив папку `my_app` в якій буде знаходитись мій проект. Створив папку `tests` де будуть тести на перевірку працездатності мого проекту. Скопіював файли `my_app/templates/index.html`, `my_app/app.py `, `my_app/requirements.txt`, `tests/conftest.py`, `tests/requirements.txt`, `tests/test_app.py` з репозиторію викладача у відповідні папки мого репозеторію. Ознайомився із вмістом кожного з файлів. Звернув увагу на файл requirements.txt у папці проекту та тестах. Даний файл буде мітити залежності для мого проекту він містить назви бібліотек які імпортуються.
#### 6. Я спробував чи проект є працездатним перейшовши у папку `my_app` та після ініціалізації середовища виконав команди записані нижче:
```text
sudo pipenv --python 3.8
sudo pipenv install -r requirements.txt
sudo pipenv run python app.py
```
1. Так само я ініціалузував середовище для тестів у іншій вкладці шелу та запустив їх командою `sudo pipenv run pytest test_app.py --url http://localhost:5000` але спочатку треба перейти в папку `tests`:
```text
    ybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5/tests$ sudo pipenv run pytest test_app.py --url http://localhost:5000
============================================ test session starts =============================================
platform linux -- Python 3.8.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /home/rybolov/tpis/Yurii-Rybak-IK-31/lab_5/tests
collected 4 items                                                                                            

test_app.py ..FF                                                                                       [100%]

================================================== FAILURES ==================================================
_________________________________________________ test_logs __________________________________________________

url = 'http://localhost:5000'

    def test_logs(url):
        response = requests.get(url + '/logs')
>       assert 'My Hostname is:' in response.text, 'Logs do not have Hostname'
E       AssertionError: Logs do not have Hostname
E       assert 'My Hostname is:' in '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...en(\'logs/app.log\', \'r\') as log:\nFileNotFoundError: [Errno 2] No such file or directory: \'logs/app.log\'\n\n-->\n'
E        +  where '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...en(\'logs/app.log\', \'r\') as log:\nFileNotFoundError: [Errno 2] No such file or directory: \'logs/app.log\'\n\n-->\n' = <Response [500]>.text

test_app.py:27: AssertionError
_______________________________________________ test_main_page _______________________________________________

url = 'http://localhost:5000'

    def test_main_page(url):
        response = requests.get(url)
>       assert 'You are at main page.' in response.text, 'Main page without text'
E       AssertionError: Main page without text
E       assert 'You are at main page.' in '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...)\nredis.exceptions.ConnectionError: Error -3 connecting to redis:6379. Temporary failure in name resolution.\n\n-->\n'
E        +  where '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...)\nredis.exceptions.ConnectionError: Error -3 connecting to redis:6379. Temporary failure in name resolution.\n\n-->\n' = <Response [500]>.text

test_app.py:32: AssertionError
========================================== short test summary info ===========================================
FAILED test_app.py::test_logs - AssertionError: Logs do not have Hostname
FAILED test_app.py::test_main_page - AssertionError: Main page without text
======================================== 2 failed, 2 passed in 0.44s =========================================
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5/tests$ ^C                                                        
```
2. Звернув увагу, що в мене автоматично створюються файли `Pipfile` та `Pipfile.lock`, а також на хост машині буде створена папка `.venv`. Після зупинки проекту видалив їх.
3. Перевірив роботу сайту перейшовши головну сторінку. Сайт не працює бо на відсутній `redis`.

#### 7. Видалив файли які постворювались після тестового запуску. Щоб моє середовище було чистим, все буде створюватись і виконуватись всередині Docker. Створив два файла `Dockerfile.app`, `Dockerfile.tests` та `Makefile` який допоможе автоматизувати процес розгортання.
#### 8. Скопіював вміст файлів `Dockerfile.app`, `Dockerfile.tests` та `Makefile` з репозиторію викладача та ознайомився із вмістом `Dockerfile` та `Makefile` та його директивами. 
Вміст файла `Dockerfile.app`:
```text
FROM python:3.8-slim
LABEL author="Rybak Yura"
# оновлюємо систему та встановлюємо потрібні пакети
RUN apt-get update \
    && apt-get upgrade -y\
    && apt-get install git -y\
    && pip install pipenv
WORKDIR /app
# Копіюємо файл із списком пакетів які нам потрібно інсталювати
COPY my_app/requirements.txt ./
RUN pipenv install -r requirements.txt
# Копіюємо наш додаток
COPY my_app/ ./
# Створюємо папку для логів
RUN mkdir logs
EXPOSE 5000
ENTRYPOINT pipenv run python app.py
```
Вміст файла `Dockerfile.tests`:
```text
FROM python:3.8-slim
LABEL author="Rybak Yura"
# оновлюємо систему та встановлюємо потрібні пакети
RUN apt-get update \
    && apt-get upgrade -y\
    && apt-get install git -y\
    && pip install pipenv
WORKDIR /tests
# Копіюємо файл із списком пакетів які нам потрібно інсталювати
COPY tests/requirements.txt ./
RUN pipenv install -r requirements.txt
# Копіюємо нашого проекту
COPY tests/ ./
ENTRYPOINT pipenv run pytest test_app.py --url http://app:5000
```
Вміст файла `Makefile`:
```text
STATES := app tests
REPO := rybakyurii/lab_4
.PHONY: $(STATES)
$(STATES):
	@docker build -f Dockerfile.$(@) -t $(REPO):$(@) .
run:
	@docker network create --driver=bridge appnet \
	&& docker run --rm --name redis --net=appnet -d redis \
	&& docker run --rm --name app --net=appnet -p 5000:5000 -d $(REPO):app
test-app:
	@docker run --rm -it --name test --net=appnet $(REPO):tests
	
docker-prune:
	@docker rm $$(docker ps -a -q) --force || true \
	&& docker container prune --force \
	&& docker volume prune --force \
	&& docker network prune --force \
	&& docker image prune --force
```
Дерективи `app` та `tests`:
Створення імеджів для сайту та тесту відповідно.
Деректива `run`:
Запускає сторінку сайту.
Деректива `test-app`:
Запуск тесту сторінки.
Деректива `docker-prune`:
Очищення іміджів, контейнера і інших файлів без тегів.
#### 9. Для початку, використовуючи команду `sudo make app` створіть Docker імеджі для додатку та для тестів `sudo make tests`. Теги для цих імеджів є з моїм Docker Hub репозиторієм. Запустив додаток командою `sudo make run` та перейшовши в іншу вкладку шелу запустіть тести командою `sudo make test-app`.
Запуск сайту
```text
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ sudo make run 
ccdd44079fafc04274fa29d8e5e0cc126934f4ee11faa1a4e04a02c104402328
Unable to find image 'redis:latest' locally
latest: Pulling from library/redis
e5ae68f74026: Already exists 
37c4354629da: Pull complete 
b065b1b1fa0f: Pull complete 
6954d19bb2e5: Pull complete 
6333f8baaf7c: Pull complete 
f9772c8a44e7: Pull complete 
Digest: sha256:2f502d27c3e9b54295f1c591b3970340d02f8a5824402c8179dcd20d4076b796
Status: Downloaded newer image for redis:latest
0734b28e4d6abfd9e3a94ff691c0a386bc39a0095aba94ff0f87e7e68872f33d
3091b8e739764187933709bb96df11ff8cb003cde9493d57d443e8824d6a401e

```
Проходження тесту:
```text
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ sudo make test-app
============================================ test session starts =============================================
platform linux -- Python 3.8.12, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /tests
collected 4 items                                                                                            

test_app.py ....                                                                                       [100%]

============================================= 4 passed in 0.32s ==============================================
```

#### 10. Зупинив проект натиснувши Ctrl+C та почистив всі ресурси `Docker` за допомогою `make`.
```text
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ sudo make docker-prune
3091b8e73976
0734b28e4d6a
438c464c4f52
Total reclaimed space: 0B
Deleted Volumes:
6ea103b2ed4b83be089541bd07bf581f7d6807bc7c10c80fc17725fe93392601

Total reclaimed space: 0B
Deleted Networks:
appnet

Total reclaimed space: 0B
```

#### 11. Створив директиву `docker-push` в Makefile для завантаження створених імеджів у мій Docker Hub репозиторій.
Деректива `docker-push`:
```text
docker-push:
	@docker login \
	&& docker push $(REPO):app \
	&& docker push $(REPO):tests
```

#### 12. Видалив створені та закачані імеджі. Команда `docker images` виводить пусті рядки. Створив директиву в Makefile яка автоматизує процес видалення моїх імеджів.
Деректива `images-delete`:
```text
images-delete:
	@docker rmi $$(docker images -q)
```
Запуск:
```text
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ sudo docker images
REPOSITORY         TAG          IMAGE ID       CREATED         SIZE
rybakyurii/lab_4   tests        00c032c0e435   6 minutes ago   300MB
rybakyurii/lab_4   app          8bc3f2996e23   7 minutes ago   299MB
rybakyurii/lab_4   monitoring   7b29f402b61b   3 hours ago     331MB
rybakyurii/lab_4   django       1a37bdd7a9b5   3 hours ago     331MB
redis              latest       aea9b698d7d1   2 days ago      113MB
python             3.8-slim     1e46b5746c7c   2 days ago      122MB
docker/whalesay    latest       6b362a9f73eb   6 years ago     247MB
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ 
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ 
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ 
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ sudo make images-delete
Untagged: rybakyurii/lab_4:tests
Deleted: sha256:00c032c0e4355b23cb65bb9f875abb9cfb63bc28658bb7df7dfe5a483bb06fb0
Deleted: sha256:8db4059a982135d69e99d0252492a64bac00181b50e59092c65d2b33cc873ade
Deleted: sha256:eabc002b44efde3a2b43034c333c31fc2348317cae111a5cc6b44736d7325891
Deleted: sha256:446d78c73f2c9fcedfec5f6080d038de5ef4976797e9e1942a65a6c12bd31d38
Deleted: sha256:e3c33a53f831b3f8bbb296c37b5021f861920d67f09c595b567a37197742225f
Deleted: sha256:67f262c7d5479e207967ea8c5852eb9044ea6398c748a2c675177893629209d5
Deleted: sha256:eb305a2fca34fd6418dcc7ad6141030aa3a7988b93911983028bd67f62b3bd6e
Deleted: sha256:2bd765a9eb648081c8899153b5ee2ab31a9aa074b1e164d76f79fb2f9f9906c1
Deleted: sha256:e955fb3859dbe3fa7ebbd484d324883ef5356d0f9e4a43ac252452d25a401d05
Untagged: rybakyurii/lab_4:app
Deleted: sha256:8bc3f2996e23d4ade2706042799a501865f7abd00fc5722860fa37996cdbb9b2
Deleted: sha256:865a56f42af89d8063c05d801a59cfaf4f521f40efe3f548e270343ff9b38d18
Deleted: sha256:3da6315612b6acc25a408f2d9900fbeeba31fad2b3314cbf96b14b6986f9719a
Deleted: sha256:28997735b67197c27ddcd148badf2d5479c33df374725d38a67fe6cec4cf06c5
Deleted: sha256:de9826a9aa3b79fae4fa8791cbdc52c012eb9851046afbfe6de314bd4f699578
Deleted: sha256:648657d7b8a401b6fc9fd08f21d896f8ce3f2d44879a069365536dc7fd3a4077
Deleted: sha256:5b0500d0067f116705396d76e42b4378014d22965eadc45612271eba1772bc7f
Deleted: sha256:6ab2f5d6aa7adb60ab7eb0ae9e9ee7f3d9499a882781a06a78ef648ab174a364
Deleted: sha256:1617bf70c03cb2e751fa74f8057fc634e30ec5d1e0fea04abd968a05a9efff84
Deleted: sha256:c336294f3b7967efe92e92db88d87f31c3d50509b78096e267d3e79d9dc276a5
Deleted: sha256:6b8bef5323bc87f8ad348723378df0b4e09d1aba5481bf91aa0791fdadaf0186
Deleted: sha256:c9b75fca937c6da3eb74122e688ceaed47a3bb15788e473b44ac8b527ae9d2a1
Deleted: sha256:e86c26d93de70cd45e59804ac4aec0f40613892e5252c57428f9a72afc6e1a66
Deleted: sha256:8ace50c3de9ec867d176cb1516ee96ec2f68279d9b3503d2558b2faade7be6e8
Deleted: sha256:6116de7faadd6da3cc3cb21eeda55d1a27f516cb316398e89084dcf8c5e8e4e9
Untagged: rybakyurii/lab_4:monitoring
Untagged: rybakyurii/lab_4@sha256:86fe874348c22b7f1e7c5f99cac9c4571c316a92db82a6f3da0cd54c0c2df5a4
Deleted: sha256:7b29f402b61b2caec127892a4f1d351846e3aa3d7ea2df10de23dd391a2bb998
Untagged: rybakyurii/lab_4:django
Untagged: rybakyurii/lab_4@sha256:4274cffbbee6eac8299d18fcbfbb7e5dc584d17ccc9f64f10452d453cd1e0804
Deleted: sha256:1a37bdd7a9b525b8935b6462bb737328e4d20da627e06020a49d931fc1ed93f4
Deleted: sha256:bac020aeb71135309eb2f8f34906f87c3ccd3a7959393c833e9b94dd84279d55
Deleted: sha256:4cfd87070049495e681693ab23179ec1ea2e8ecb47f271eeb98f7ee13a8da966
Deleted: sha256:3104b25b53b791a1aa4ab8fb4608ece3c72aedf1ba97734fca1d0f2783ed682b
Deleted: sha256:203bcc311d759567eb83ee9b09e7fb035bbc0e72dfc2f5b466adfd4d01eb4107
Deleted: sha256:c7b1a2b5eadbbc42be244cb32a270089e383b8795aa94fb3559b3cb355146faa
Deleted: sha256:d329235ad6ea58724480a4d97ebadb330fbb669bc523d20464789932a8b99315
Deleted: sha256:e701194bceaa9372792dad3f097f079d11cc1f2420e6b06bfc8b20c9dbf886ca
Deleted: sha256:87608bbe0b630f3b764bafaed848cfc00fa0cfafcf43c568b149752b153741dd
Deleted: sha256:79bb62c23a0346d12878e9eab08df6450284e0289ba8778c04df030164bad32a
Deleted: sha256:6c0ecb97f03ea37955898c95e714695d7b242b3698405fe3a491f6e718c74fff
Deleted: sha256:666fceb826f7ddd5677b9342da1d0e25fa74b1f62c25e759572008e67efb4f8e
Deleted: sha256:0948733b124df50d9b5d931c9ab7c76b9e4a5c6628a9bd20b4974f4b2f772544
Deleted: sha256:983d7f469967cf0833fa3272a872c3246b706b2d1db02b6bfac9b7d4e7064c06
Deleted: sha256:ca452e977711137347096f7f2a7aee7d57eb76d48a07f7eab796bccf56f66c4d
Deleted: sha256:3b6778f3f1a3f6b5fef3fd2b275689ff0896c1a26b92fde6ce0b98fb74c9a806
Deleted: sha256:d63fc23b37c5a9717c0acbcc3bdccd22849270abd4da6a1225b93e9415201346
Deleted: sha256:2315e45e75eae6fa93083610259bd3b27ea7457c0e989eeb01b051a84462bea4
Untagged: redis:latest
Untagged: redis@sha256:2f502d27c3e9b54295f1c591b3970340d02f8a5824402c8179dcd20d4076b796
Deleted: sha256:aea9b698d7d1d2fb22fe74868e27e767334b2cc629a8c6f9db8cc1747ba299fd
Deleted: sha256:beb6c508926e807f60b6a3816068ee3e2cece7654abaff731e4a26bcfebe04d8
Deleted: sha256:a5b5ed3d7c997ffd7c58cd52569d8095a7a3729412746569cdbda0dfdd228d1f
Deleted: sha256:ee76d3703ec1ab8abc11858117233a3ac8c7c5e37682f21a0c298ad0dc09a9fe
Deleted: sha256:60abc26bc7704070b2977b748ac0fd4ca94b818ed4ba1ef59ca8803e95920161
Deleted: sha256:6a2f1dcfa7455f60a810bb7c4786d62029348f64c4fcff81c48f8625cf0d995a
Untagged: python:3.8-slim
Untagged: python@sha256:0f6d6953c6612786ed05aaf1de7151dbbb0cea6bc83687040d5f15377be7ef64
Deleted: sha256:1e46b5746c7c53dafaa00f1c8c7f5aaee28bcbf5c13e60ea338f3607efe1281d
Deleted: sha256:4085d78a1998f4cdb3744213b30fd050bfff8982f34e47f52f850b3015227b1e
Deleted: sha256:ed5ddd0966fc584af5654636ccd64194290741760c34948feda1d8f6b786c769
Deleted: sha256:ab7b3af28da29d0c73ed2b805868ac1bfa1c21ecb6f1ed4db2893583ee532a3e
Deleted: sha256:e5e2fb86d700299ae660f69c7c81bc48d0091f0fcbeddf4f6e6290de4993fa5d
Deleted: sha256:9321ff862abbe8e1532076e5fdc932371eff562334ac86984a836d77dfb717f5
Untagged: docker/whalesay:latest
Untagged: docker/whalesay@sha256:178598e51a26abbc958b8a2e48825c90bc22e641de3d31e18aaf55f3258ba93b
Deleted: sha256:6b362a9f73eb8c33b48c95f4fcce1b6637fc25646728cf7fb0679b2da273c3f4
Deleted: sha256:34dd66b3cb4467517d0c5c7dbe320b84539fbb58bc21702d2f749a5c932b3a38
Deleted: sha256:52f57e48814ed1bb08a651ef7f91f191db3680212a96b7f318bff0904fed2e65
Deleted: sha256:72915b616c0db6345e52a2c536de38e29208d945889eecef01d0fef0ed207ce8
Deleted: sha256:4ee0c1e90444c9b56880381aff6455f149c92c9a29c3774919632ded4f728d6b
Deleted: sha256:86ac1c0970bf5ea1bf482edb0ba83dbc88fefb1ac431d3020f134691d749d9a6
Deleted: sha256:5c4ac45a28f91f851b66af332a452cba25bd74a811f7e3884ed8723570ad6bc8
Deleted: sha256:088f9eb16f16713e449903f7edb4016084de8234d73a45b1882cf29b1f753a5a
Deleted: sha256:799115b9fdd1511e8af8a8a3c8b450d81aa842bbf3c9f88e9126d264b232c598
Deleted: sha256:3549adbf614379d5c33ef0c5c6486a0d3f577ba3341f573be91b4ba1d8c60ce4
Deleted: sha256:1154ba695078d29ea6c4e1adb55c463959cd77509adf09710e2315827d66271a
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ 
```

#### 13. Перейшов до іншого варіанту з використанням `docker-compose.yaml`. Для цього створив даний файл у кореновій папці проекту та заповнив вмістом з прикладу. Проект який я буду розгортити за цим варіантом трохи відрізняється від першого тим що у нього зявляється дві мережі: приватна і публічна.
Файл `docker-compose.yaml`:
```text
version: '3.8'
services:
  hits:
    build:
      context: .
      dockerfile: Dockerfile.app
    image: rybakyurii/lab_4:compose-app
    container_name: app
    depends_on:
      - redis
    networks:
      - public
      - secret
    ports:
      - 80:5000
    volumes:
      - hits-logs:/hits/logs
  tests:
    build:
      context: .
      dockerfile: Dockerfile.tests
    image: rybakyurii/lab_4:compose-tests
    container_name: tests
    depends_on:
      - hits
    networks:
      - public
  redis:
    image: redis:alpine
    container_name: redis
    volumes:
      - redis-data:/data
    networks:
      - secret
volumes:
  redis-data:
    driver: local
  hits-logs:
    driver: local
networks:
  secret:
    driver: bridge
  public:
    driver: bridge
```

#### 14. Перевірив чи `Docker-compose` встановлений та працює у моїй системі, а далі просто запускаю `docker-compose`:
```text
docker-compose --version
sudo docker-compose -p lab5 up
```
```text
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ docker-compose --version
docker-compose version 1.29.2, build 5becea4c

```

#### 15. Перевірив чи працює веб-сайт. Дана сторінка відображається за адресою `http://172.19.0.2:5000/`:

#### 16. Перевірив чи компоуз створив докер імеджі. Всі теги коректні і назва репозиторія вказана коректно:
```text
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ sudo docker images
REPOSITORY         TAG             IMAGE ID       CREATED         SIZE
rybakyurii/lab_4   compose-tests   00d2747a480e   2 minutes ago   300MB
rybakyurii/lab_4   compose-app     a18c877b7c26   3 minutes ago   299MB
python             3.8-slim        1e46b5746c7c   2 days ago      122MB
redis              alpine          3900abf41552   5 days ago      32.4MB
rybolov@rybolov-VirtualBox:~/tpis/Yurii-Rybak-IK-31/lab_5$ 
```

#### 17. Зупинив проект натиснувши `Ctrl+C` і почистітив ресурси створені компоуз командою `docker-compose down`.

#### 18. Завантажив створені імеджі до Docker Hub репозиторію за допомого команди `sudo docker-compose push`.

#### 19. Що на Вашу думку краще використовувати `Makefile` чи `docker-compose.yaml`? - На мою думку `Makefile` при використанні більш інтуїтивно зрозумілий, адже можна в ньому побачити які команди запускаються, але і в одночас треба знати які команди використовувати. На рахунок `docker-compose.yaml` він менш зрозуміліший і там не показано команди які потрібно запустити а лише вказано що потрібно запусти, підклучити чи збілдити і користувача не хвилює як воно це робить. Як для мене мені обидва методи добрі.

#### 20. (Завдання) Оскільки Ви навчились створювати docker-compose.yaml у цій лабораторній то потрібно:
- Cтворив `docker-compose.yaml` для лабораторної №4. Компоуз повинен створити два імеджі для `Django` сайту та моніторингу, а також їх успішно запустити.
Файлик `docker-compose.yaml`:
```text
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: rybakyurii/lab_4:compose-jango
    container_name: django
    networks:
      - public
    ports:
      - 8000:8000
  monitoring:
    build:
      context: .
      dockerfile: Dockerfile.site
    image: rybakyurii/lab_4:compose-monitoring
    container_name: monitoring
    network_mode: host
networks:
  public:
    driver: bridge
```
#### 21. Після успішного виконання роботи я відредагував свій `README.md` у цьому репозиторію та створив pull request.
