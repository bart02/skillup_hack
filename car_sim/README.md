# Настройка импровизированного робоавтомобиля
Чтобы скачать проект на сервер выполните команду 
```bash
git clone https://github.com/bart02/skillup_hack
``` 

Установить на устройство необходимые библиотеки
```bash
cd skillup_hack/car_sim
pip install -r requirements.txt
```

При необходимости (отсутствии PyPi пакетов), собрать OpenCV версии 4.*.* из исходников по инстуркциям https://www.pyimagesearch.com/opencv-tutorials-resources-guides/.

Изменить адрес сервера в 97 строке
```python
URL = 'http://car.batalov.me'  # Without slash at the end
```

Изменить источник видеопотока в 117 строке
```python
cap = cv2.VideoCapture('aa123.avi')
```
