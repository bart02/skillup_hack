# Настройка импровизированного робоавтомобиля
Чтобы скачать проект на сервер выполните команду 
```bash
git clone https://github.com/bart02/skillup_hack
``` 

Установить на устройство необходимые библиотеки
```bash
cd skillup_hack/car
pip install -r requirements.txt
```

Cобрать OpenCV версии 4.*.* из исходников по инстуркциям https://www.pyimagesearch.com/opencv-tutorials-resources-guides/, в зависимости от используемого устройства и ОС.

Изменить адрес сервера в 112 строке
```python
URL = 'http://car.batalov.me'  # Without slash at the end
```

Изменить источник видеопотока в 132 строке
```python
cap = cv2.VideoCapture('aa123.avi')
```

Указать IP просмотрщика видеопотока в 17 строке
```python
footage_socket.connect('tcp://ip:5555')
```
