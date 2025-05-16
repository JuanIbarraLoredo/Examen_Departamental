const int sensorLuz = A0;
const int foco1 = 2;
const int foco2 = 3;
const int foco3 = 4;

int limiteLuz = 200;

String datosSerial = "";

void setup() {
  pinMode(foco1, OUTPUT);
  pinMode(foco2, OUTPUT);
  pinMode(foco3, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char caracter = Serial.read();
    if (caracter == '\n') {
      interpretarOrden(datosSerial);
      datosSerial = "";
    } else {
      datosSerial += caracter;
    }
  }

  int intensidadLuminosa = analogRead(sensorLuz);
  Serial.print(intensidadLuminosa);
  Serial.print("-");
  Serial.print(intensidadLuminosa);
  Serial.print("-");
  Serial.print(intensidadLuminosa);
  Serial.println("-");

  if (intensidadLuminosa < limiteLuz) {
    digitalWrite(foco1, HIGH);
    digitalWrite(foco2, HIGH);
    digitalWrite(foco3, HIGH);
  } else {
    digitalWrite(foco1, LOW);
    digitalWrite(foco2, LOW);
    digitalWrite(foco3, LOW);
  }

  delay(500);
}

void interpretarOrden(String orden) {
  if (orden.startsWith("UMBRAL:")) {
    String numeroStr = orden.substring(7);
    int umbralNuevo = numeroStr.toInt();
    if (umbralNuevo > 0 && umbralNuevo < 1024) {
      limiteLuz = umbralNuevo;
      Serial.print("Límite actualizado: ");
      Serial.println(limiteLuz);
    }
  }
}
