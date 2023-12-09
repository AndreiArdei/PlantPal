// Global definitions
#define NUM_SENSORS 2
#define AVG_SAMPLES 10
#define ADC_RESOLUTION 10

// LDR definitions
#define LDR_PIN 0
#define LDR_RESISTOR 47000
#define LDR_MULT 32017200.0
#define LDR_POW 1.5832

// Soil Moisture Sensor definitions
#define SOIL_PIN 1

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValues[NUM_SENSORS] = {0, 0};

  // Take AVG_SAMPLES samples
  for (int i = 0; i < AVG_SAMPLES; i++ ) {
    for (int sensor = 0; sensor < NUM_SENSORS; sensor++) {
      sensorValues[sensor] += analogRead(sensor);
    }
  }

  // Take average of samples
  for (int sensor = 0; sensor < NUM_SENSORS; sensor++) {
    sensorValues[sensor] /= AVG_SAMPLES;
  }

  // Calculate lux value for LDR
  float ratio = ((float)pow(2, ADC_RESOLUTION) / (float)sensorValues[LDR_PIN]) - 1;
  sensorValues[LDR_PIN] = LDR_MULT / (float)pow(LDR_RESISTOR / ratio, LDR_POW);

  // Write samples
  for (int sensor = 0; sensor < NUM_SENSORS; sensor++) {
    int value = sensorValues[sensor];
    Serial.print(sensor);
    Serial.print(":");
    Serial.println(value);
  }
}
