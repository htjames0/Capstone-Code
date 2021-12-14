OPC opc;

color white = color(255,255,255);
color black = color(0,0,0);
color r = color(255,0,0);
color g = color(0,255,0);
color b = color(0,0,255);

color[] modes = new color[]{white,r,g,b};

int curLed = 0;
int mode = 0;
int ledsPerStrip = 64;
int numStrips = 5;
int numLeds = ledsPerStrip * numStrips;

void keyPressed() { 
    if(key == CODED){
        if(keyCode == RIGHT){
            mode++;
            mode = mode%modes.length;
        }
        if(keyCode == LEFT){
            mode--;
            if(mode <= -1){
                mode = modes.length-1;
            }
        }
    }
}


void setup(){

  //gui
  size(500,500);
  textSize(128);
  rectMode(CENTER);
  //endgui
  opc = new OPC(this, "127.0.0.1", 7890);
  colorMode(RGB,100);
  frameRate(10);
}

void draw(){
    //gui
    background(modes[mode]);
    stroke(black);
    fill(black);
    text("" + curLed, 250,250);
    //endgui

    int s = second();
    if (s%2 == 0){
        println("Second is even");
        for(int i = 0; i < numLeds; i++){
            opc.setPixel(i, modes[mode]);
        }
    }
    else{
        println("Second is odd");
        for(int i = 0; i < numLeds; i++){
            opc.setPixel(i, black);
        }
    }
    opc.writePixels();
}
