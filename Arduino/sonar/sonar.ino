#include <NewPing.h>

int echoPin = 2; 
int trigPin = 3;
char inputData = ' ';
NewPing np(trigPin, echoPin);

void setup() {
  // put your setup code here, to run once:
  Serial.begin (115200); 
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    inputData = Serial.read();
    //Serial.println(inputData);
    if(inputData == '1'){
      double duration, cm;
    
      duration = np.ping_median(50);
      cm = duration / 58;
      Serial.print("data=");
      Serial.println(cm);
    }
  }
}
