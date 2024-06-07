float freq=1000.0;
void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT);
//  setPWM(60000);
  pinMode(10, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  delay(10);
}

void loop() {
  if(Serial.available() > 1){
    freq=Serial.parseFloat();
    Serial.println(freq);
  }
  setPWM(freq);
//  for(float i=10.0;i<60000.0;i+=1){
//    setPWM(i);
//    int x=map(i,0,60000,0,3000);
//    Serial.println(x);
//    delay(1);
//  }
//  for(float i=60000.0;i>=10.0;i-=1){
//    setPWM(i);
//    int x=map(i,0,60000,0,3000);
//    Serial.println(x);
//    delay(1);
//  }
  
}

void setPWM(float frequency) {
  
  float period = 1.0 / frequency;
  int prescaler = 1;
  float counts = (float)F_CPU / prescaler * period - 1;
  int duty = counts * 0.5; 

  TCCR1A = _BV(COM1A1) | _BV(COM1A0) | _BV(WGM11);
  TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS10); 
  ICR1 = (int)counts;
  OCR1A = duty;
}
