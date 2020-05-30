#include <WiFi.h>
#include <HTTPClient.h>

#include <Servo.h>
Servo myservo;

const char* ssid     = "dir-300";
const char* password = "Level123";

void setup() {
  Serial.begin(115200);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  myservo.attach(4);

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) {
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    if (http.begin("http://car.batalov.me/s")) {  // HTTP
      Serial.print("[HTTP] GET...\n");
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        if (httpCode == HTTP_CODE_OK) {
          String payload = http.getString();
          Serial.println(payload);
          if  (payload == "0") {
            myservo.write(0);
            Serial.println("[Servo] close");
          }
          else if (payload == "1") {
            myservo.write(90);
            Serial.println("[Servo] open");
          }
        }
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        myservo.write(50);
        Serial.println("[Servo] err");
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }

  delay(100);
}
