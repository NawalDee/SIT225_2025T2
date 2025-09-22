#include "arduino_secrets.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <WiFiConnectionHandler.h>
#include <ArduinoIoTCloud.h>
#include "thingProperties.h"


#define DHTPIN 2     
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// PIR Sensor
#define PIR_PIN 3    

//  Ultrasonic Sensor 
#define TRIG_PIN 4
#define ECHO_PIN 5

// LEDs 
#define LED_RED 6
#define LED_GREEN 7

void setup() {
  Serial.begin(9600);
  delay(1500); 

  //  IoT Cloud
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  //  sensors
  dht.begin();
  pinMode(PIR_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  //  LEDs
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);

  Serial.println("System started...");
}

void loop() {
  ArduinoCloud.update();

  //  DHT11 readings 
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (!isnan(temp)) temperature = temp;
  if (!isnan(hum)) humidity = hum;

  //  PIR readings 
  pIR_Motion = digitalRead(PIR_PIN);

  //  Ultrasonic readings 
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 20000);
  distance = (duration > 0) ? duration * 0.034 / 2 : -1;

  //  LED Alerts 
  bool danger = false;

  if (temperature > 30) danger = true;       
  if (pIR_Motion == LOW) danger = true;      
  if (distance > 0 && distance < 20) danger = true; 

  if (danger) {
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, LOW);
    alert = 1;
  } else {
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_GREEN, HIGH);
    alert = 0;
  }

  // Debug prints 
  Serial.print("Temp: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.print(" %, PIR: ");
  Serial.print(pIR_Motion);
  Serial.print(", Distance: ");
  Serial.print(distance);
  Serial.print(" cm, Alert: ");
  Serial.println(alert);

  delay(2000);
}
