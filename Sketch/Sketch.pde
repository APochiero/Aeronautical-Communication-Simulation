
// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

int N = 20;
int BS = 5;
int M = BS-1;
int t = 10;
float offset = 0.1;
float gridWidth = 0.8;
// A Aircraft object
Aircraft[] aircrafts;
BaseStation[] bs;
void setup() {
  size(800, 800);
  aircrafts = new Aircraft[N];
  bs = new BaseStation[BS*BS];
  for ( int i = 0; i < N; i++ ) 
    aircrafts[i] = new Aircraft(offset);
  for ( int i = 0; i < BS; i++ ) {
    for ( int j = 0; j < BS; j++ ) {
      bs[i*BS+j] = new BaseStation(i, j, M);
    }
  }
}

void draw() {
  background(255);
  fill(180);
  stroke(0);
  strokeWeight(1);
  rect(width*offset, height*offset, width*gridWidth, height*gridWidth );
  for ( int i = 0; i < BS; i++ ) {
    line(width*offset+(i*width*gridWidth/M), height*offset, width*offset+(i*width*gridWidth/M), height-height*offset);
    line(width*offset, height*offset+(i*width*gridWidth/M), width-width*offset, height*offset+(i*width*gridWidth/M));
  }
  for ( int i = 0; i < BS; i++ ) {
    for ( int j = 0; j < BS; j++ ) {
      bs[i*BS+j].display();
    }
  }
  for ( int i = 0; i < N; i++ ) {
    // Update the position
    aircrafts[i].update();
    // Display the Aircraft
    aircrafts[i].display(); 
    pushMatrix();
    translate(aircrafts[i].position.x, aircrafts[i].position.y);
    PVector min = PVector.sub(bs[0].position, aircrafts[i].position);
    for ( int k = 0; k < BS; k++ ) {
      for ( int j = 0; j < BS; j++ ) {
        if (PVector.sub(bs[k*BS+j].position, aircrafts[i].position).mag() < min.mag() ) {
          min = PVector.sub(bs[k*BS+j].position, aircrafts[i].position);
          if ( frameCount < 2 || frameCount%(t*60) == 0 ) {
            aircrafts[i].serverBS = bs[k*BS+j].position;
          }
        }
      }
    }
    PVector anchor = PVector.sub(aircrafts[i].serverBS, aircrafts[i].position);
    stroke(255, 0, 0);
    strokeWeight(1);
    line(0, 0, min.x, min.y);
    stroke(0,255,0);
    strokeWeight(2);
    line(0, 0, anchor.x, anchor.y);
    popMatrix();
  }
}
