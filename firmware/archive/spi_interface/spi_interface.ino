unsigned char test[1000];
byte marker = 0;

/***************************************************************
  Setup SPI in slave mode (1) define MISO pin as output (2) set
  enable bit of the SPI configuration register
****************************************************************/
void setup() {
  // put your setup code here, to run once:
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);

}

void loop() {
  // put your main code here, to run repeatedly:

  char test[] = "This is a test for CG3002";
  if ((SPSR & (1 << SPIF)) != 0) {
    SPDR = test[marker];
    marker++;
    if (marker > sizeof(test)) {
      marker = 0;
    }
  }
}
