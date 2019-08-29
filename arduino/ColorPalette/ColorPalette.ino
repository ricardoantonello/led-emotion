/* Este código foi extraído de um exemplo de FastLED chamado ColorPalette
 * Adaptado por ricardo@antonello.com.br 
 */

#include <FastLED.h>

#define LED_PIN     8
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define UPDATES_PER_SECOND 100

#define NUM_LEDS 264 //nao consegui transformar em variavel para mudar via serial no python....
int BRIGHTNESS = 120; //era constante alterei pra variavel para poder mudar por serial vindo do python

CRGB leds[NUM_LEDS];


// This example shows several ways to set up and use 'palettes' of colors
// with FastLED.
//
// These compact palettes provide an easy way to re-colorize your
// animation on the fly, quickly, easily, and with low overhead.
//
// USING palettes is MUCH simpler in practice than in theory, so first just
// run this sketch, and watch the pretty lights as you then read through
// the code.  Although this sketch has eight (or more) different color schemes,
// the entire sketch compiles down to about 6.5K on AVR.
//
// FastLED provides a few pre-configured color palettes, and makes it
// extremely easy to make up your own color schemes with palettes.
//
// Some notes on the more abstract 'theory and practice' of
// FastLED compact palettes are at the bottom of this file.



CRGBPalette16 currentPalette;
TBlendType    currentBlending;

extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;

//Global Antonello
int comando_serial=0; // 0=rainbow 0=Vermelho... etc.. 

void setup() {
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    
    currentPalette = RainbowColors_p;
    currentBlending = LINEARBLEND;

    //Codigo Antonello
    Serial.begin(9600);
    Serial.setTimeout(1); // em milis, fundamental para nao atrasar o Serial.parseInt()
    pinMode(LED_BUILTIN, OUTPUT);
}


void loop()
{
    ChangePalettePeriodically();
    
    static uint8_t startIndex = 0;
    startIndex = startIndex + 1; /* motion speed */
    
    FillLEDsFromPaletteColors( startIndex);
    
    FastLED.show();
    FastLED.delay(1000 / UPDATES_PER_SECOND);
}

void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
    uint8_t brightness = 255;
    
    for( int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}


// There are several different palettes of colors demonstrated here.
//
// FastLED provides several 'preset' palettes: RainbowColors_p, RainbowStripeColors_p,
// OceanColors_p, CloudColors_p, LavaColors_p, ForestColors_p, and PartyColors_p.
//
// Additionally, you can manually define your own color palettes, or you can write
// code that creates color palettes on the fly.  All are shown here.

void ChangePalettePeriodically()
{
    uint8_t secondHand = (millis() / 1000) % 60;
    static uint8_t lastSecond = 99;
    
  /*
    if( lastSecond != secondHand) {
        lastSecond = secondHand;
        if( secondHand ==  0)  { currentPalette = RainbowColors_p;         currentBlending = LINEARBLEND; }
        if( secondHand == 10)  { currentPalette = RainbowStripeColors_p;   currentBlending = NOBLEND;  }
        if( secondHand == 15)  { currentPalette = RainbowStripeColors_p;   currentBlending = LINEARBLEND; }
        if( secondHand == 20)  { SetupPurpleAndGreenPalette();             currentBlending = LINEARBLEND; }
        if( secondHand == 25)  { SetupTotallyRandomPalette();              currentBlending = LINEARBLEND; }
        if( secondHand == 30)  { SetupBlackAndWhiteStripedPalette();       currentBlending = NOBLEND; }
        if( secondHand == 35)  { SetupBlackAndWhiteStripedPalette();       currentBlending = LINEARBLEND; }
        if( secondHand == 40)  { currentPalette = CloudColors_p;           currentBlending = LINEARBLEND; }
        if( secondHand == 45)  { currentPalette = PartyColors_p;           currentBlending = LINEARBLEND; }
        if( secondHand == 50)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = NOBLEND;  }
        if( secondHand == 55)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = LINEARBLEND; }
    }
*/

/* Código Antonello

    REFERENCIA DE CORES
    Red (0..) "HUE_RED"
    Orange (32..) "HUE_ORANGE"
    Yellow (64..) "HUE_YELLOW"
    Green (96..) "HUE_GREEN"
    Aqua (128..) "HUE_AQUA"
    Blue (160..) "HUE_BLUE"
    Purple (192..) "HUE_PURPLE"
    Pink(224..) "HUE_PINK"   
    
    if( lastSecond != secondHand) {
        lastSecond = secondHand;
        if( secondHand ==  0)  { currentPalette = RainbowColors_p;         currentBlending = LINEARBLEND; }
        if( secondHand == 10)  { SetupCor(0,10,20);   }
        if( secondHand == 15)  { SetupCor(44,54,34); }
        if( secondHand == 20)  { SetupCor(86,96,76); }
        if( secondHand == 25)  { SetupCor(160,120,170); }
        
    }
*/

  // Leitura da Serial
  if (Serial.available() > 0) {
    digitalWrite(LED_BUILTIN, HIGH); //liga led
    comando_serial = Serial.parseInt();
    //Serial.println(comando_serial);
  }
  
  if(comando_serial==0){
    currentPalette = RainbowColors_p;         
    currentBlending = LINEARBLEND;
  }else if(comando_serial==1){
    SetupCor(0,10,20); /*Vermelho*/
  }else if(comando_serial==2){
    SetupCor(44,54,34); /*Amarelo*/
  }else if(comando_serial==3){
    SetupCor(86,96,76); /*Verde*/
  }else if(comando_serial==4){
    SetupCor(160,120,170); /*Azul*/ 
  }else if(comando_serial==5){
    SetupBlackAllPalette(); /*Desligados*/ 
    
  
  //NAO FUNCIONOU
  }else if(comando_serial==11){ //aumenta brilho//NAO FUNCIONOU
    BRIGHTNESS=BRIGHTNESS+50; //NAO FUNCIONOU
    //FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    //FastLED.setBrightness(  BRIGHTNESS );    
  }else if(comando_serial==12){ //diminui brilho
    BRIGHTNESS=BRIGHTNESS-50;
    //FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    //FastLED.setBrightness(  BRIGHTNESS );    
  
  
  }else{
    Serial.print("ERRO: comando serial desconhecido! Recebido: "); 
    Serial.println(comando_serial); 
  }
}

// This function fills the palette with totally random colors.
void SetupTotallyRandomPalette()
{
    for( int i = 0; i < 16; i++) {
        currentPalette[i] = CHSV( random8(), 255, random8());
    }
}

// This function sets up a palette of black and white stripes,
// using code.  Since the palette is effectively an array of
// sixteen CRGB colors, the various fill_* functions can be used
// to set them up.
void SetupBlackAndWhiteStripedPalette()
{
    // 'black out' all 16 palette entries...
    fill_solid( currentPalette, 16, CRGB::Black);
    // and set every fourth one to white.
    currentPalette[0] = CRGB::White;
    currentPalette[4] = CRGB::White;
    currentPalette[8] = CRGB::White;
    currentPalette[12] = CRGB::White;
    
}

void SetupBlackAllPalette() //todos desligados
{
    fill_solid( currentPalette, 16, CRGB::Black);
}

// This function sets up a palette of purple and green stripes.
void SetupPurpleAndGreenPalette()
{
    CRGB purple = CHSV( HUE_PURPLE, 255, 255);
    CRGB green  = CHSV( HUE_GREEN, 255, 255);
    CRGB black  = CRGB::Black;
    
    currentPalette = CRGBPalette16(
                                   green,  green,  black,  black,
                                   purple, purple, black,  black,
                                   green,  green,  black,  black,
                                   purple, purple, black,  black );
}

//Metodos criados por Antonello
void SetupCor(int a, int b, int c)
{
    currentBlending = LINEARBLEND;
    CRGB corA = CHSV( a, 255, 255);
    CRGB corB = CHSV( b, 255, 255);
    CRGB corC = CHSV( c, 255, 255);
    currentPalette = CRGBPalette16(
                                   corA,  corB,  corA,  corB,
                                   corA,  corC,  corA,  corC,
                                   corA,  corB,  corA,  corB,
                                   corA,  corC,  corA,  corC
                                   );
}

//Fim de métodos Antonello

// This example shows how to set up a static color palette
// which is stored in PROGMEM (flash), which is almost always more
// plentiful than RAM.  A static PROGMEM palette like this
// takes up 64 bytes of flash.
const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM =
{
    CRGB::Red,
    CRGB::Gray, // 'white' is too bright compared to red and blue
    CRGB::Blue,
    CRGB::Black,
    
    CRGB::Red,
    CRGB::Gray,
    CRGB::Blue,
    CRGB::Black,
    
    CRGB::Red,
    CRGB::Red,
    CRGB::Gray,
    CRGB::Gray,
    CRGB::Blue,
    CRGB::Blue,
    CRGB::Black,
    CRGB::Black
};


// Additional notes on FastLED compact palettes:
//
// Normally, in computer graphics, the palette (or "color lookup table")
// has 256 entries, each containing a specific 24-bit RGB color.  You can then
// index into the color palette using a simple 8-bit (one byte) value.
// A 256-entry color palette takes up 768 bytes of RAM, which on Arduino
// is quite possibly "too many" bytes.
//
// FastLED does offer traditional 256-element palettes, for setups that
// can afford the 768-byte cost in RAM.
//
// However, FastLED also offers a compact alternative.  FastLED offers
// palettes that store 16 distinct entries, but can be accessed AS IF
// they actually have 256 entries; this is accomplished by interpolating
// between the 16 explicit entries to create fifteen intermediate palette
// entries between each pair.
//
// So for example, if you set the first two explicit entries of a compact 
// palette to Green (0,255,0) and Blue (0,0,255), and then retrieved 
// the first sixteen entries from the virtual palette (of 256), you'd get
// Green, followed by a smooth gradient from green-to-blue, and then Blue.
