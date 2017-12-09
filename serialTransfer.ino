/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

 This example code is in the public domain.
 */

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(57600);
  //Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  //digitalWrite(8,LOW);
  //char c = Serial.read();
  
  //if (c == '5'){
    //digitalWrite(8, HIGH);
      while (true){  
        Serial.println(analogRead(A0));
        delay(0.0001);
        //Serial.println(analogRead(A1)*10);
        //Serial.println(analogRead(A2)*100);
    //}
  }
  //delay(0.01);        // delay in between reads for stability
}
