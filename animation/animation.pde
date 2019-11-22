//<>// //<>//
import garciadelcastillo.dashedlines.*;

/* ANIMATION SETTINGS */
int N = 1;             // number of aircrafts
int BS = 2;            // base stations on a row
int t = 60;            // handover period
float offset = 0.1;    // percentage of left and right margin of the grid
float gridWidth = 0.8; // percentage of grid's width wrt windows width 
float T = 0.001;       // serviceTime constant
float p = 180;          // penalty time
int maxQueued = 0;
DashedLines dash;

/* Automatically calculated parameters */
int M = BS*BS-1;          // intervals between base stations in a row
float leftBorder;
float rightBorder; 
float upperBorder;
float bottomBorder;

float outerLeftBorder; 
float outerRightBorder; 
float outerUpperBorder; 
float outerBottomBorder; 

Aircraft[] aircrafts;
BaseStation[] bs;

/* SETUP */
void setup() {
  size(800, 800);
  leftBorder = width*offset+width*gridWidth/(2*M);
  rightBorder = width*gridWidth-width*gridWidth/(2*M);
  upperBorder = height*offset+height*gridWidth/(2*M);
  bottomBorder =  height-height*offset-height*gridWidth/(2*M);

  outerLeftBorder = width*offset;
  outerRightBorder = width*gridWidth;
  outerUpperBorder = height*offset;
  outerBottomBorder =  height*gridWidth;

  aircrafts = new Aircraft[N];
  bs = new BaseStation[BS*BS];
  for ( int i = 0; i < N; i++ ) 
    aircrafts[i] = new Aircraft();
  for ( int i = 0; i < BS; i++ ) {
    for (int j = 0; j < BS; j++ ) {
      bs[i*BS+j] = new BaseStation(i, j);
    }
  }
  // Initialize it, passing a reference to the current PApplet
  dash = new DashedLines(this);

  // Set the dash-gap pattern in pixels
  dash.pattern(10, 5);
}

void draw() {
  /* PREPARE FIELD */
  background(255);  // background color
  stroke(0);        // lines
  strokeWeight(1);  // lines tickness

  /* main field rectangle (filled) */
  fill(200);        // inner-grid color
  float x = width*offset+(width*gridWidth/(2*M));
  float y = height*offset+(height*gridWidth/(2*M));
  float w = width*gridWidth-width*gridWidth/M;
  float h = height*gridWidth-height*gridWidth/M;
  dash.rect(x, y, w, h);

  /* grid lines */
  for (int i = 0; i < BS*BS; i++) {
    line(width*offset+(i*width*gridWidth/M), height*offset, width*offset+(i*width*gridWidth/M), height-height*offset);
    line(width*offset, height*offset+(i*width*gridWidth/M), width-width*offset, height*offset+(i*width*gridWidth/M));
  }

  /* draw BS at intersection of grid lines */
  for ( int i = 0; i < BS; i++ ) {
    for ( int j = 0; j < BS; j++ ) {
      bs[i*BS+j].display();
    }
  }

  /* Aircraft Loop */
  for ( int i = 0; i < N; i++ ) {  /* for each AC... */
    aircrafts[i].update();   // update AC position
    aircrafts[i].display();  // display AC 
    pushMatrix();
    translate(aircrafts[i].position.x, aircrafts[i].position.y);
    /* compute minimum distance between AC and BS */
    PVector min = PVector.sub(bs[0].position, aircrafts[i].position);
    for ( int k = 0; k < BS; k++ ) {
      for ( int j = 0; j < BS; j++ ) {
        if (PVector.sub(bs[k*BS+j].position, aircrafts[i].position).mag() < min.mag() ) {
          min = PVector.sub(bs[k*BS+j].position, aircrafts[i].position);
          if ( frameCount < 10 || frameCount%t == 0 ) {
            if ( aircrafts[i].serverBS.id != bs[k*BS+j].id ) {
              aircrafts[i].serverBS = bs[k*BS+j];
              aircrafts[i].waiting = true;
              aircrafts[i].waitingFrame = frameCount;
              println("Handover");
            }
          }
        }
      }
    }

    /* show nearest BS connection */
    PVector anchor = PVector.sub(aircrafts[i].serverBS.position, aircrafts[i].position);
    stroke(0, 255, 0);
    strokeWeight(1);
    line(0, 0, min.x, min.y);

    /* show current BS connection */

    // show blue connection when sending packet
    if ( aircrafts[i].queued > 0 && !aircrafts[i].sending ) {
      if ( aircrafts[i].queued > maxQueued ) {
        maxQueued = aircrafts[i].queued;
      }
      aircrafts[i].serviceTime = T*pow(anchor.mag(), 2);
      aircrafts[i].sendingFrame = frameCount-1;
      aircrafts[i].queued--;
      aircrafts[i].sending = true;
    }

    if ( aircrafts[i].waiting && frameCount%aircrafts[i].waitingFrame <= p ) {
      stroke(255, 255, 0);
    } else {
      aircrafts[i].waiting = false;
      stroke(255, 0, 0);
    }

    // keep connection blue for serviceTime seconds otherwise red and update serving state
    if ( aircrafts[i].sending && frameCount%aircrafts[i].sendingFrame <= aircrafts[i].serviceTime ) {
      stroke(0, 0, 255);
    } else {
      aircrafts[i].sending = false;
      stroke(255, 0, 0);
    }
    strokeWeight(2);
    line(0, 0, anchor.x, anchor.y);
    popMatrix();
  }
}
