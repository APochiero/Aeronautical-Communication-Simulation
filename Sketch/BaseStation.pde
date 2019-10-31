

class BaseStation {
  PVector position;
  int row;
  int col;
  int M;

  BaseStation( int row, int col, int M) {
    this.row = row;
    this.col = col;
    this.M = M;
    position = new PVector(width*0.1+(col*width*0.8/M), height*0.1+(row*width*0.8/M));
  }

  void display() {
    fill(255, 255, 0);
    circle(width*0.1+(col*width*0.8/M), height*0.1+(row*width*0.8/M), 10);
  }
}
