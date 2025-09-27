#include <Arduino_LSM6DS3.h>   
#include <WiFiNINA.h>
#include <ArduinoMqttClient.h>


char ssid[] = "NetComm 3225 2.4GHz";   
char pass[] = "decefacuwa";

const char broker[] = "e13ebf470e3c4a198cdd8d9b62d911b7.s1.eu.hivemq.cloud";
int port = 8883;   


const char mqttUsername[] = "nawal";
const char mqttPassword[] = "Test1234@";

WiFiSSLClient wifiClient;       
MqttClient mqttClient(wifiClient);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi!");

  
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  mqttClient.setId("nawalArduino01");   
  mqttClient.setUsernamePassword(mqttUsername, mqttPassword);

 
  Serial.print("Connecting to MQTT broker...");
  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    while (1);   
  }
  Serial.println("Connected to HiveMQ!");
}

void loop() {
  float x, y, z;

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);

    
    mqttClient.beginMessage("nawal/gyro");
    mqttClient.print(x);
    mqttClient.print(",");
    mqttClient.print(y);
    mqttClient.print(",");
    mqttClient.print(z);
    mqttClient.endMessage();

    Serial.print("Published: ");
    Serial.print(x);
    Serial.print(", ");
    Serial.print(y);
    Serial.print(", ");
    Serial.println(z);
  }

  delay(200);  // every 0.2 seconds
}
