OPC opc;
PImage dot;
int w = 10;
int h = 6;
int spacing = 50;

void setup()
{
  size(spacing*(w+2), spacing*(h+2));

  // Load a sample image
  dot = loadImage("color-dot.png");

  // Connect to the local instance of fcserver
  opc = new OPC(this, "127.0.0.1", 7890);
  opc.ledGrid(0, 10, 6, width/2, height/2, spacing, spacing, 0, false);
}

void draw()
{
  background(0);

  // Draw the image, centered at the mouse location
  float dotSize = width * 0.5;
  image(dot, mouseX - dotSize/2, mouseY - dotSize/2, dotSize, dotSize);
}

