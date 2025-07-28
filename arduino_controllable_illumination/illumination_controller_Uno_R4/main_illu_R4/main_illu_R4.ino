/*
 FWest Arduino UNO R4 Wifi v01.08.2023
 Setting up a UART communication between the Bruker NMR-Spectrometer PC and LED.
 No Spectrometer modification required
 Instructions to the Arduino are sent as 8-bit integer numbers,
 separated by space (" ").

 !!! Only applies to Uno R3 / MEGA2560:
 !!! A 10 uF or 22 uF electrolyte cap has to be conneected between RESET (+) and GND(-)
 !!! on the Arduino to prevent resetting when Serial ports are opened!
 !!! Only works properly with the capacitor connected!
 !!! R4 Wifi does not need this as it seems

 The number of received arguments with this code depends on the Baudrate.
 9600: 11-15 bytes can be received without problem (e.g. 255 255 255 == 11 bytes == 11.5 ms)
 115200: At least 128 bytes can be received

 Known Bugs:
 - Sent messages are printed wrong sometimes at higher Baudrates when using PySerial,
   this may be an Error of Python, though since it is always correct in the Arduino IDE
   serial monitor.
   v01.08.2023 for R4: This error does not occur
 - Communication is sometimes randomly not working anymore, the Rx/Tx LEDs turn on
   for a few seconds, but nothing is sent back and sent commands are not executed (22.05.2023)
   fix from:
   https://stackoverflow.com/questions/34694052/why-serial-communications-from-arduino-stops-after-some-time
   Apparently this can be accounted to voltage fluctuations, etc.

Version Changes:
 - 22.05.2023: Added regular reset of Serial port, controlled by RESETRATE and indicted by a short
               flashing of the builtin LED.
               Added zeroing the gcaRxStr to 0x00 with memset
 - 01.08.2023: Using the 8x12 LED-matrix on the Uno R4 Wifi to visualize the set PWM-Level.
*/

#include <string.h>
#include <stdlib.h>
#include "Arduino_LED_Matrix.h"
#include <EEPROM.h>

#define BAUDRATE 115200                       // Baudrate, on some systems the value 9600 may be used 
#define PWM_PIN 9                             // Physical Pin Number on Arduino, must be PWM compatible (UNO R3: 3, 5, 6, 9, 10, 11)
#define MAX_MESSAGE_LENGTH 64                 // Max allowed length of input
#define ARG_NUMBER 10                         // Max allowed number of args, higher baudrates allow more args
#define RESETRATE 10000                       //  Set port reset rate in ms. (i.e. each approx. RESETRATE ms, the port will be closed and reopened)

static char gcaRxStr[MAX_MESSAGE_LENGTH+1];   // Received message string
static char * gcaAux;                         // Auxiliary String for strtok() string splitting
static uint8_t u8aArgs[ARG_NUMBER];           // Arguments as Array
static uint8_t u8pwm = 0;                     // PWM duty cycle variable
static uint8_t u8RxStrPos = 0;                // Position at Received string, equals to number of rec. bytes
static uint8_t u8ArgPos = 0;                  // Number of Arguments after strtok() splitting
static uint32_t u32reset = 0;                 // Resetcounter for port closing and reopening

// R4 Specific code
ArduinoLEDMatrix matrix;
uint32_t status[3];

void setup() 
{
  Serial.begin(BAUDRATE); 
  matrix.begin();
  while(!Serial) continue; // This evaluates to always true on Uno R3
  pinMode(PWM_PIN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  delay(10);

  // The if statement prints a string permanently stored in EEPROM (Starting from address 0x0000), if present
  // The EEPROM can be written by another Arduino program.
  // New Arduinos have all bytes initialized to 0xFF
  if (EEPROM.read(0x0000) != 0xFF)
  {
    uint16_t u16address =0x0000;
    while (EEPROM.read(u16address) != 0xFF)
    {
      Serial.print(char(EEPROM.read(u16address)));
      u16address++;
    }
    Serial.println();
  }
  Serial.print("Starting...");
  Serial.println();
}

void loop()
{
  // READ UART INPUT
  char cInByte;

  if (Serial.available() > 0)
  {
    delay(1);
    u8RxStrPos = 0;
    u8ArgPos = 0;
    memset(gcaRxStr, 0, MAX_MESSAGE_LENGTH+1); // Reset the character argument string
    while (Serial.available() > 0)
    {
      cInByte = Serial.read();
      if (cInByte != '\n')
      {
        gcaRxStr[u8RxStrPos] = cInByte;
        u8RxStrPos++;
      }
      if (cInByte == '\n')
      {
        gcaRxStr[u8RxStrPos] = '\0';
        u8RxStrPos = 0;
      }
    } // End of message receive code


    // The UART has been read, now we can evaluate the string
    // The string is being split into substrings with strtok() and each arg converted to int,
    // then stored into u8aArgs Array. u8ArgPos holds the number of given arguments (like argc)
    gcaAux = strtok(gcaRxStr, " "); // First argument
    u8aArgs[u8ArgPos] = atoi(gcaAux);
    u8ArgPos++;
    while( gcaAux != NULL )  // Loop through as long as there are args
    {
      //Serial.println(gcaAux); //printing each token
      gcaAux = strtok(NULL, " ");
      u8aArgs[u8ArgPos] = atoi(gcaAux);
      u8ArgPos++;
    }
    Serial.print("Received: ");
    for (int i = 0 ; i < u8ArgPos-1; i++)
    {
      Serial.print(i);
      Serial.print(":");
      Serial.print(u8aArgs[i]);
      Serial.print(", ");
    } // At this point we have u8aArgs Array ready, and can do something with it
    Serial.println("");
    delay(3);
    

    /// COMMANDS
    switch (u8aArgs[0]) // The first argument is evaluated, type == int !!!, no "" needed
    {
      case (0): // Switch PWM off completely
        analogWrite(PWM_PIN,0); break;
      case (1): // Switch / updatePWM on to u8pwm value
        analogWrite(PWM_PIN, u8pwm); break;
      case (2): // Change PWM duty cycle variable
        u8pwm = u8aArgs[1]; break;
      case (3): // Change PWM duty cycle and update output
        u8pwm = u8aArgs[1]; analogWrite(PWM_PIN, u8pwm); break;
      case (4): // Toggle the OUTPUT 0% 100%
        u8pwm = (u8pwm > 0) ? 0 : 255; analogWrite(PWM_PIN, u8pwm); break;
      // More cases / commands can be added here to do whatever is needed 
      default:
      break;
    }
  
  } 

  // Start of Uno R4 Wifi specific code to control LED-Matrix on board
  uint8_t temp = uint8_t( (float(u8pwm)/255) * 96);
  status[0] = 0x00000000;
  status[1] = 0x00000000;
  status[2] = 0x00000000;
  for (int i = 0; i < 96; i++)
  {
    if (u8pwm != 0)
    {
      status[2] |= (1 << 0);
    }
    if (i < 32)
    {
      if (temp > 0)
      {
        status[2] |= (1 << i);
        temp--;
      }
    }
    else if (i < 64)
    {
      if (temp > 0)
      {
        status[1] |= (1 << (i-32));
        temp--;
      }
    }
    else
    {
      if (temp > 0)
      {
        status[0] |= (1 << (i-64));
        temp--;
      }
    }
  }
  matrix.loadFrame(status);
  // End of UNO R4 Wifi specific code

  // Reopening port unconditionally
  // Voltage fluctuations can cause the serial communication to break
  // This is a fix to obtain higher stability during runtime
  if(u32reset == RESETRATE) 
  {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.end();      // close serial port
    delay(1);        //wait 1 ms
    Serial.begin(BAUDRATE); // reenable serial again
    delay(10);
    digitalWrite(LED_BUILTIN, LOW);
    u32reset = 0;
  }
  u32reset++;
  delay(1);
}

