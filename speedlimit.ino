#define sensorpin  2    // wielsensor aangesloten op pin 2
#define lamppin    3    // achterlicht aangesloten op pin 3
#define motorpin   4    // Motor aangesloten op pin 4
#define ledpin     13

int lampstatus;
int laatstelampstatus;
long laatstelamptijd;
int begrenzer = true;

int sensorstatus; 
int laatstesensorstatus;
boolean laatstehogepulse = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  pinMode(sensorpin, INPUT);
  pinMode(lamppin, INPUT);
  pinMode(motorpin, OUTPUT);
  pinMode(ledpin, OUTPUT);
  //digitalWrite(lamppin, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  checkLamp();
  checkSensor();
}

void checkLamp(){
// Deze functie checkt of de lamp aan / of uit is en zet het programma begrenzer aan of uit.
  lampstatus = digitalRead(lamppin);
  if (lampstatus == HIGH && laatstelampstatus == LOW){ 
    // Lamp is aan, was uit, en de begrenzer is actief.
    Serial.println("Lichtpulse ontvangen. Interval:");
    unsigned long lampinterval = (millis() - laatstelamptijd);
    Serial.print(lampinterval);
    
    if(lampinterval <= 2000 && lampinterval >= 100){
      if( begrenzer == true){
        Serial.println("Begrenzer gedeactiveerd");
        begrenzer = false;
      }else{
        Serial.println("Begrenzer geactiveerd");
        begrenzer = true;
      }
      laatstelamptijd = millis();
    }else if(lampinterval >= 2000){
      // Lamp is voor het laatst gewisseld, meer dan 2 seconden gelezen dus reset de timer.
      laatstelamptijd = millis();
    }
    delay(10);
    laatstelampstatus = lampstatus;
  }
  else{
    laatstelampstatus = lampstatus;  
  } 
}

void checkSensor(){
  // We geven alleen de pulsen door, niet als hij continu hoog is.
  sensorstatus = digitalRead(sensorpin);
   if(sensorstatus == HIGH && laatstesensorstatus == LOW){
     // Sensor is hoog, was laag. 
     Serial.println("Hoge pulse");
     if(laatstehogepulse == false){
       // De laatse hoge pulse is niet verzonden, we verzenden deze dus wel.
       laatstehogepulse = true;
       sendPulse();
     }
     else{
       laatstehogepulse = false;  
     } 
      laatstesensorstatus = sensorstatus;   
   } 
   else if (sensorstatus == LOW && laatstesensorstatus == HIGH){
     // Sensor is laag, was hoog.
     Serial.println("Lage pulse");
     laatstesensorstatus = sensorstatus;
 }
}

void sendPulse()
{
   Serial.println("Sending pulse");
   digitalWrite(motorpin, HIGH);
   digitalWrite(ledpin, HIGH);
//	unsigned long intervalPulse = 500; // wait for 500 miliseconds.
//	static unsigned long previousMillisPulse;

//	if( millis() - previousMillisPulse > intervalPulse ) {
//		previousMillisPulse = millis();
delay(200);
		digitalWrite(motorpin, LOW);
                digitalWrite(ledpin, LOW);
               
//	}
//delay(20);
}
