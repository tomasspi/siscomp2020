**Para instalar Python 3.8:**

```shell
sudo apt update
sudo apt install software-properties-common
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
sudo add-apt-repository ppa:deadsnakes/ppa
```

Apretar `[ENTER]` para que se añada el repositorio

```shell
sudo apt install python3.8
```
**Correr el siguiente comando:**

```shell
pip3 --version
```

Verificar al final de lo que tira que la version de python sea la 3.8.3.
Sino es asi, ejecutar todos los comandos con pip o python en adelante asi:

```shell
pip3.8
python3.8
```

**Para instalar librerias del programa:**

```shell
pip3 install requests
pip3 install django
```

**Para ejecutar:**

```shell
cd /buttonpython/
python3 manage.py runserver 127.0.0.1:8002
```
o
```shell
python manage.py runserver 127.0.0.1:8002
```
Si no tira error con ingresar a esa `ip:puerto` deberia abrir una pag
