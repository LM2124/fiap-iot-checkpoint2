#define LED1_PIN 4
#define LED2_PIN 5
#define LED3_PIN 6
#define LED4_PIN 7
#define LED5_PIN 8
#define LED6_PIN 9
#define LED7_PIN 10
#define LED8_PIN 11
#define LED9_PIN 12
#define LED10_PIN 13

void setup() {
  // put your setup code here, to run once:
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(LED3_PIN, OUTPUT);
  pinMode(LED4_PIN, OUTPUT);
  pinMode(LED5_PIN, OUTPUT);
  pinMode(LED6_PIN, OUTPUT);
  pinMode(LED7_PIN, OUTPUT);
  pinMode(LED8_PIN, OUTPUT);
  pinMode(LED9_PIN, OUTPUT);
  pinMode(LED10_PIN, OUTPUT);
  Serial.begin(9600);
  display();
}

int setAmt = 3;
void display() {
  bool led1 = ((setAmt & 1) == 1);
  bool led2 = ((setAmt & 2) == 2);
  bool led3 = ((setAmt & 4) == 4);
  bool led4 = ((setAmt & 8) == 8);
  bool led5 = ((setAmt & 16) == 16);
  bool led6 = ((setAmt & 32) == 32);
  bool led7 = ((setAmt & 64) == 64);
  bool led8 = ((setAmt & 128) == 128);
  bool led9 = ((setAmt & 256) == 256);
  bool led10 = ((setAmt & 512) == 512);
  digitalWrite(LED1_PIN, led1 ? HIGH : LOW);
  digitalWrite(LED2_PIN, led2 ? HIGH : LOW);
  digitalWrite(LED3_PIN, led3 ? HIGH : LOW);
  digitalWrite(LED4_PIN, led4 ? HIGH : LOW);
  digitalWrite(LED5_PIN, led5 ? HIGH : LOW);
  digitalWrite(LED6_PIN, led6 ? HIGH : LOW);
  digitalWrite(LED7_PIN, led7 ? HIGH : LOW);
  digitalWrite(LED8_PIN, led8 ? HIGH : LOW);
  digitalWrite(LED9_PIN, led9 ? HIGH : LOW);
  digitalWrite(LED10_PIN, led10 ? HIGH : LOW);
  Serial.println(setAmt);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char c = Serial.read();
    Serial.println(c);
    if (c == 'W') {
      // increment
      setAmt++;
      display();
    } else if (c == 'A') {
      // shift left
      setAmt = setAmt >> 1;
      display();
    } else if (c == 'S') {
      // decrement
      setAmt--;
      display();
    } else if (c == 'D') {
      // shift right
      setAmt = setAmt << 1;
      display();
    } else if (c == 'R') {
      // reset
      setAmt = 0;
      display();
    }
  }
  delay(100);
}