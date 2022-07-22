#include "EEPROM.h"
#include "mString.h"
mString<60> buf;
#define devicename "Arduino"
bool waitForData = false;
bool waitForReadBlock = false;
bool waitForWriteBlock = false;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(2000000);
  Serial.println("10 INIT");
  Serial.println("5 INFO");
  Serial.println(devicename);
  Serial.println("6 INFOEND");
}

void readBlock(mString<60> buf) {
  Serial.println("5 INFO");
  Serial.println(String(eeprom_read_byte((buf.toInt())), HEX));
  Serial.println("6 INFOEND");
  waitForReadBlock = false;
}

void writeBlock(int addr, int val) {
  //EEPROM.update(buf.toInt(), val.toInt());
  eeprom_write_byte(addr,val);
  Serial.println("15 OK");
  waitForWriteBlock = false;
  Serial.setTimeout(10);
}
mString<60> inputString;
mString<60> input;
mString<60> firstVal;
mString<60> secondVal;
bool waitforRead = true;
void loop() {
  
  // put your main code here, to run repeatedly:
  while (Serial.available()) {
    //inputString = Serial.read();
    if(waitforRead == true){
      inputString+=char(Serial.read());
      if(inputString.indexOf("\n") == -1){}else{
          waitforRead = false;
          inputString.remove(inputString.indexOf("\r\n"), 2);
          inputString.remove(inputString.indexOf("\n"), 1);
              if (inputString == "20 READ") {
      Serial.println("15 OK");
      waitForReadBlock = true;
      waitForData = true;
      //
    } else if (inputString == "30 CLEAR") {
      int EEPROMlength = EEPROM.length();
      for (int i = 0; i < EEPROMlength; i++) EEPROM.update(i, 0);
      Serial.println("15 OK");
    } else if (inputString == "35 RESET") {
      int EEPROMlength = EEPROM.length();
      for (int i = 0; i < EEPROMlength; i++) EEPROM.update(i, 255);
      Serial.println("15 OK");
    }else if (inputString == "3 SIZE") {
      Serial.println("5 INFO");  
      Serial.println(EEPROM.length());
      Serial.println("6 INFOEND");
    } else if (inputString == "21 READALL") {
      Serial.println("5 INFO");
      int EEPROMlength = EEPROM.length();
      for (int i = 0; i < EEPROMlength; i++){
       char hexadecimalnum [5];
       sprintf(hexadecimalnum, "%02X", eeprom_read_byte(i));
       Serial.print(hexadecimalnum);
       Serial.print(" ");
      }
      Serial.println("\n6 INFOEND");
    } else if (inputString == "25 WRITE") {
      Serial.println("15 OK");
      waitForWriteBlock = true;
      waitForData = true;
    } else if (inputString == "5 INFO") {
      buf = "";
      Serial.println("15 OK");
      waitForData = true;
    } else if (inputString == "6 INFOEND") {
      Serial.println("15 OK");
      waitForData = false;
      if (waitForReadBlock) {
        readBlock(buf);
      } else if (waitForWriteBlock) {
        int data[60];
        input = buf.parseInts(data,60,','); 
        writeBlock(data[0],data[1]);
      }
      
    } else {
      if (waitForData) {
        buf += inputString;
        Serial.println("15 OK");
      } else {
        Serial.println("0 UNKNOWN");
      }
    }
    waitforRead = true;
    inputString.clear();
      }
    }
  }
}
