OPC opc;

int lightsPerStrip = 64; //50
int numStrips = 5;
int numLights = lightsPerStrip * numStrips;

int guiSize = 500;

color[] lightState = new color[numLights];
PVector[] lightLocation = new PVector[numLights];

PImage curImage;

int guiScaleFactor;

void readMap(String fileName){
  Table map = loadTable(fileName, "header, csv");
  //for each element in the file
    //figure out the array location aka. light adress
    //create a vector according to the angle
    //set the mag of that vector according to distance (aka d)
    for (TableRow row : map.rows()){
      int id = row.getInt("light address");
      int d = row.getInt("d");
      int theta = row.getInt("theta"); 
      int theta_reverse = row.getInt("theta reverse");
      
      PVector vec = PVector.fromAngle(radians(theta));
      vec.setMag(d);
      lightLocation[id] = vec;
      
    }  

}


void scaleLocationsToImage(PImage img){  //maps 2D image to 3D space
  int r = img.width/2;
  float max = 0;
  for(PVector curLoc : lightLocation){
    if(curLoc.mag() > max){
      max = curLoc.mag();
    }
  }
  for(PVector curLoc : lightLocation){
   curLoc.setMag((curLoc.mag()/max) * r);
  }
}

void mapImageToLights(PImage img){     // maps 3D space to lights 
  img.loadPixels();
  int r = img.width/2;
  
  for(int i = 0; i < numLights; i++){
    //vectors are assumed scaled to image size
    PVector curLoc = lightLocation[i];
    lightState[i] = img.pixels[  (int(curLoc.y) + r) * img.width + Math.round(curLoc.x) + r ];
  }
}


void setup(){    
  
  //gui
  size(500,500);
  //end gui

  
  for(int i = 0; i < numLights; i++){
    lightState[i] = color(0,0,0);
    lightLocation[i] = new PVector(0,0);
  }

  readMap("ledmap.csv");
  
  curImage = loadImage("blueANDgreen.png");

  opc = new OPC(this, "127.0.0.1", 7890);
  frameRate(10);
  colorMode(RGB, 100);
  
  noSmooth();
  guiScaleFactor = guiSize/curImage.width;
  scaleLocationsToImage(curImage);
  mapImageToLights(curImage);

}

void draw(){
  background(0,0,0);
  image(curImage, 0, 0, guiSize, guiSize);
  int r = curImage.width/2 * guiScaleFactor;
  for(int i = 0; i < numLights; i++){
   stroke(0);
   strokeWeight(10);
   fill(lightState[i]);
   circle(lightLocation[i].x * guiScaleFactor + r, lightLocation[i].y * guiScaleFactor + r, 10);
   opc.setPixel(i, lightState[i]);
  }
  opc.writePixels();
}
