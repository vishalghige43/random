#include <Arduino.h>

String msg; 
String start="start";
String stop="stop";
String mode1="mode1";
String mode2="mode2";



void setup() {
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  Serial.begin(9600);

  
}

void loop() {
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);

  if(Serial.available())msg=Serial.readStringUntil('\n');
  
  
  if(msg==start)digitalWrite(8,LOW);
  if(msg==stop)digitalWrite(9,LOW);
  if(msg==mode1)digitalWrite(10,LOW);
  if(msg==mode2)digitalWrite(11,LOW);

  start+=(char)13;
  stop+=(char)13;
  mode1+=(char)13;
  mode2+=(char)13;

  if(msg==start)digitalWrite(8,LOW);
  if(msg==stop)digitalWrite(9,LOW);
  if(msg==mode1)digitalWrite(10,LOW);
  if(msg==mode2)digitalWrite(11,LOW);

}
