

class BaseStation {
  PVector position;
  int row;
  int col;
  int id;

  BaseStation( int row, int col) {
    this.row = row;
    this.col = col;
    position = new PVector(width*offset+(col*width*0.8/M) + width*0.8/M, height*0.1+(row*width*0.8/M) + height*0.8/M);
    id = (row*2+col)+1;
  }

  void display() {
    textSize(32);
    textAlign(CENTER);
    pushMatrix();
    fill(250, 22, 95);
    text(id, position.x, position.y- 20 );

    fill(255, 255, 0);
    circle(position.x,position.y, 10);
    popMatrix();
  }
}
