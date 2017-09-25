int led = 12;
void setup() { 
  Serial.begin(9600);
  pinMode(led, OUTPUT); 
  pinMode(A1, OUTPUT);
  pinMode(A0, OUTPUT);
}
void loop() {
  digitalWrite(led, HIGH); 
  Serial.print("A1: ");
  Serial.println(analogRead(A1));
  Serial.print("A0: ");
  Serial.println(analogRead(A0));
  Serial.println(" ");
  delay(1000); 
  digitalWrite(led, LOW); 
  Serial.print("A1: ");
  Serial.println(analogRead(A1));
  Serial.print("A0: ");
  Serial.println(analogRead(A0));
  Serial.println(" ");
  delay(1000); 
}
