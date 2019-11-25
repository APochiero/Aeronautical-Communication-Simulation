class Aircraft { //<>//
  // The Aircraft tracks position, velocity, and acceleration 
  PVector position;
  PVector velocity;
  PVector acceleration;
  PVector desiredPosition;
  BaseStation serverBS;
  BaseStation nearestBS;
  int tick;
  PImage img;
  color c;
  int size; 
  float speed;
  float serviceTime;
  boolean sending;
  boolean waiting;
  int sendingFrame;
  int waitingFrame;
  int queued;
  int nextArrival;

  Aircraft() {    
    position = new PVector(random(leftBorder, rightBorder), random(upperBorder, bottomBorder));
    velocity = new PVector(0, 0);
    acceleration = new PVector(0, 0);
    serverBS = new BaseStation(-1, -1);
    nearestBS = new BaseStation(0, 0);
    desiredPosition = new PVector(random(outerLeftBorder, outerRightBorder), random(outerUpperBorder, outerBottomBorder));
    tick = floor(random(30, 120));
    c = color(random(0, 255), random(0, 255), random(0, 255));
    size = 10;
    speed = 0.5;
    sending = false;
    waiting = false;
    queued = 0;
    sendingFrame = 0;
    nextArrival = floor((float)exp.sample()) + 10;
  }

  void update() {
    //println(queued);
    if ( frameCount % nextArrival == 0 ) { 
      queued++;
      nextArrival = floor((float)exp.sample()) + 10;
    }

    /* change desired position every tick frames */
    if ( frameCount % tick == 0 ) { 
      desiredPosition = new PVector(random(outerLeftBorder, outerRightBorder), random(outerUpperBorder, outerBottomBorder));
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
    if ( position.x >= rightBorder )
      position.x = leftBorder;
    else if ( position.x <= leftBorder )
      position.x = rightBorder;
    else if ( position.y >= bottomBorder )
      position.y = upperBorder;
    else if ( position.y <= upperBorder )
      position.y = bottomBorder;
  }

  void display() {
    stroke(0);
    strokeWeight(1);
    fill(0, 0, 255);
    //circle(desiredPosition.x, desiredPosition.y, 5 );

    pushMatrix();
    fill(c);
    translate(position.x, position.y);
    line(0, 0, velocity.x*velocity.mag()*20, velocity.y*velocity.mag()*20);
    rotate(velocity.heading());
    triangle(-size*2, -size/2, 0, 0, -size*2, size/2);
    popMatrix();
  }
}
