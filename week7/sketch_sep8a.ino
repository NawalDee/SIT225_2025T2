#include "DHT.h"

#define DHTPIN 2        // Signal pin to D2
#define DHTTYPE DHT11   // Sensor type DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT11 sensor!");
    return;
  }

  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);

  delay(2000); // DHT11 needs at least 2 sec delay
}
