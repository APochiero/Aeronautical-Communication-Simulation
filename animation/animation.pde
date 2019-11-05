/*  The Nature of Code
    Daniel Shiffman
    http://natureofcode.com */

/* ANIMATION SETTINGS */
int N = 2;             // number of aircrafts
int BS = 5;            // base stations on a row
int t = 1200;            // handover period
float offset = 0.1;     // percentage of left and right margin of the grid
float gridWidth = 0.8;  // percentage of grid's width wrt windows width 

/* Automatically calculated parameters */
int M = BS-1;          // intervals between base stations in a row

Aircraft[] aircrafts;
BaseStation[] bs;

/* SETUP */
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
  /* PREPARE FIELD */
  background(255);  // background color
  fill(180);        // inner-grid color
  stroke(0);        // lines
  strokeWeight(1);  // lines tickness
  
  /* main field rectangle (filled) */
  rect(width*offset, height*offset, width*gridWidth, height*gridWidth );
  
  /* grid lines */
  for (int i = 0; i < BS; i++) {
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
            aircrafts[i].serverBS = bs[k*BS+j].position;
          }
        }
      }
    }

    /* show nearest BS connection */
    PVector anchor = PVector.sub(aircrafts[i].serverBS, aircrafts[i].position);
    stroke(0, 255, 0);
    strokeWeight(1);
    line(0, 0, min.x, min.y);
    
    /* show current BS connection */
    if ( frameCount%aircrafts[i].k  <= 20 ) {
      stroke(255, 0, 0);
      strokeWeight(2);
      line(0, 0, anchor.x, anchor.y);
      println(aircrafts[i].k);
    }
    popMatrix();
  }
}
