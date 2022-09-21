# gost_requests
Контейнер для запросов с шифрованием GOST


Поместисть в директорию dist файлы cacer.p7b CMakeLists.txt linux-amd64_deb.tgz Рафинад.cer Рафинад.pfx

Создать файл .env, и написать в нем два параметра:
1)PATH_TO_CRYPTOPRO_CURL - путь до криптопро curl
2)CERTIFICATE_SHA1_THUMBPINT - SHA1_Thumbpint сертификата Рафинад.cer

Выполнить сборку контейнера
```
docker-compose up -d --build
```

Открыть терминал контейнера, подставив в следующую команду ID контейнера
```
docker exec -it CONTAINER_ID /bin/sh
```

Перейти в директорию /tmp/src
```
cd /tmp/src
```

Выполнить установку сертификатов следующей последовательностью команд. 
Команду "certmgr -install -store uRoot -file cacer.p7b" необходимо выполнить столько раз, 
сколько сертификатов находится в файле, при этом каждый раз указывая следующий номер устанавливаемого сертификата
```
certmgr -inst -provtype 24 -pfx -pin 123456780 -file ??????????????.pfx
certmgr -inst -store uMy -file ??????????????.cer
certmgr -install -store uRoot -file cacer.p7b
csptest -absorb -certs -autoprov
```

API готово к получению запросов



