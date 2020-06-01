# Настройка автоматических ворот
Для ESP-32 установить библиотеку https://github.com/RoboticsBrno/ServoESP32

Указать данные авторизации Wi-Fi
```cpp
const char* ssid     = "";
const char* password = "";
```

Указать адрес устройства на сервере
```cpp
if (http.begin("http://car.batalov.me/s")) {
```

Указать пин серво в соответствии с PinOut платы
```cpp
myservo.attach(4);
```