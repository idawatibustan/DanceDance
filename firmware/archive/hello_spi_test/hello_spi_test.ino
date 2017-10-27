/*************************************************************
 SPI_Hello_Raspi
   Configures an ATMEGA as an SPI slave and demonstrates
   bidirectional communication with an Raspberry Pi SPI master
   by repeatedly sending the text "Hello Raspi"
****************************************************************/


/***************************************************************
 Global Variables
  -hello[] is an array to hold the data to be transmitted
  -marker is used as a pointer in traversing data arrays
/***************************************************************/

unsigned char hello[] = {'H','e','l','l','o',' ',
                         'R','a','s','p','i','\n'};
byte marker = 0;

/***************************************************************  
 Setup SPI in slave mode (1) define MISO pin as output (2) set
 enable bit of the SPI configuration register 
****************************************************************/ 
                    
void setup (void)
{
 
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE); // equivalent to SPCR = SPCR | _BV(SPE)

}  

/***************************************************************  
 Loop until the SPI End of Transmission Flag (SPIF) is set
 indicating a byte has been received.  When a byte is
 received, load the next byte in the Hello[] array into SPDR
 to be transmitted to the Raspberry Pi, and increment the marker.
 If the end of the Hell0[] array has been reached, reset
 marker to 0.
****************************************************************/

void loop (void)
{

  if((SPSR & (1 << SPIF)) != 0)
  {
    SPDR = hello[marker];
    marker++;
   
    if(marker > sizeof(hello))
    {
      marker = 0;
    }  
  }
}
