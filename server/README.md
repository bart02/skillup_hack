# Настройка сервера
Чтобы скачать проект на сервер выполните команду 
```bash
git clone https://github.com/bart02/popkov_hackaton
``` 
Установить на устройство необходимые библиотеки
```bash
cd popkov_hackaton/server
pip install -r requirements.txt
```
Теперь можно запустить сервер написав в командную строку
```bash
python manage.py runserver 0.0.0.0:8000
```
Чтобы перейти на веб страницу наберите в адресной строке ip адрес сервера в локальной сети и укажите порт 8000 (`http://ip:8000`).