void setup() {
  Serial.begin(9600);
}


void loop() {
  String toSend = "This message was sent from Arduino MEGA";
  int strSize = sizeof(toSend);

  Serial.println(toSend);

  delay(1000);
}

