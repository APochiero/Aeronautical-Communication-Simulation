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
  int k;
  float serviceTime;
  boolean sending;
  int sendingFrame;
  int queued;

  Aircraft(float offset) {
    this.offset = offset;
    position = new PVector(random(width*offset, width-width*offset), random(height*offset, height-height*offset));
    velocity = new PVector(0, 0);
    acceleration = new PVector(0, 0);
    serverBS = new PVector(0, 0);
    desiredPosition = new PVector(random(width*offset, width-width*offset), random(height*offset, height-height*offset));
    tick = floor(random(30, 120));
    c = color(random(0, 255), random(0, 255), random(0, 255));
    size = 10;
    speed = 0.5;
    k = 20;//floor(random(20, 30));
    sending = false;
    queued = 0;
    sendingFrame = 0;
  }

  void update() {
    //println(queued);
    if ( frameCount % k == 0 ) { 
      queued++;
    }
    /* when handover procedure must be performed */
    if ( frameCount % tick == 0 ) { 
      desiredPosition = new PVector(random(width*offset, width-width*offset), random(height*offset, height-height*offset));
    }

    PVector acceleration = PVector.sub(desiredPosition, position);  // vector for new position direction
    acceleration.setMag(0.01);  // use that direction, but fix magnitude

    // Velocity changes according to acceleration
    velocity.add(acceleration);
    // Limit the velocity by topspeed
    velocity.normalize();
    velocity.mult(speed);
    // position changes by velocity
    position.add(velocity);
    if ( position.x >= width-width*offset )
      position.x = width*offset;
    else if ( position.x <= width*offset )
      position.x = width-width*offset;
    else if ( position.y >= height-height*offset )
      position.y = height*offset;
    else if ( position.y <= height*offset )
      position.y = height-height*offset;
  }

  void display() {
    stroke(0);
    strokeWeight(1);
    fill(0, 0, 255);
    circle(desiredPosition.x, desiredPosition.y, 5 );

    pushMatrix();
    fill(c);
    translate(position.x, position.y);
    line(0, 0, velocity.x*velocity.mag()*20, velocity.y*velocity.mag()*20);
    rotate(velocity.heading());
    triangle(-size*2, -size/2, 0, 0, -size*2, size/2);
    popMatrix();
  }
}
