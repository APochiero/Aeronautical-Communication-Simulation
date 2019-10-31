// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

class Aircraft {

  // The Aircraft tracks position, velocity, and acceleration 
  PVector position;
  PVector velocity;
  PVector acceleration;
  PVector desiredPosition;
  PVector serverBS;
  int tick;
  PImage img;
  color c;
  int size; 
  float offset;
  float speed;

  Aircraft( float offset) {
    this.offset = offset;
    position = new PVector(random(width*offset, width-width*offset), random(height*offset, height-height*offset));
    velocity = new PVector(0, 0);
    acceleration = new PVector(0, 0);
    serverBS = new PVector(0, 0);
    //desiredPosition = new PVector(random(width*offset, width-width*offset), random(height*offset, height-height*offset));
    desiredPosition = new PVector(random(0, width), random(0, height));
    tick = floor(random(90, 120));
    c = color(random(0, 255), random(0, 255), random(0, 255));
    size = 10;
    speed = 1;
  }

  void update() {

    //float changeCoordinate = random(0, 1);

    if ( frameCount%tick== 0 ) 
      desiredPosition = new PVector(random(0, width), random(0, height));

    PVector acceleration = PVector.sub(desiredPosition, position);
    // Set magnitude of acceleration
    acceleration.setMag(0.03);

    // Velocity changes according to acceleration
    velocity.add(acceleration);
    // Limit the velocity by topspeed
    velocity.normalize();
    velocity.mult(speed);
    // position changes by velocity
    position.add(velocity);
  }


  void display() {
    stroke(0);
    strokeWeight(1);
    fill(127);
    circle(desiredPosition.x, desiredPosition.y, 2 );

    pushMatrix();
    fill(c);
    translate(position.x, position.y);
    line(0, 0, velocity.x*velocity.mag()*20, velocity.y*velocity.mag()*20);
    rotate(velocity.heading());
    triangle(-size*2, -size/2, 0, 0, -size*2, size/2);
    popMatrix();
  }
}
