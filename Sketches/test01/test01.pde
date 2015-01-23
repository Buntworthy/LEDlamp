Boolean connected = true;

OPC opc;
PImage dot;
int w = 10;
int h = 6;
int spacing = 50;

color c1 = color(255, 20, 100);
color c2 = color(100, 20, 10);
float t = 0;

void setup()
{
  size(spacing*(w+2), spacing*(h+2));


  if (connected == true) {
    // Connect to the local instance of fcserver
    opc = new OPC(this, "127.0.0.1", 7890);
    opc.ledGrid(0, 10, 6, width/2, height/2, spacing, spacing, 0, false);
  }
}

void draw()
{
  background(0);
  c2 = color(255.0*mouseY/height, 200, 255);

//  for (int iLine = 0; iLine<height; iLine++) {
//    noFill();
//    float fac = float(iLine+mouseX)/height;// interpolation factor
//    fac = max(0, min(1, fac));
//    stroke(lerpColor(c1, c2, fac));
//    line(0, iLine, width, iLine);
//  }
  
//  for (int n=0; n<20; n++){
//    fill(180,200,255,20);
//    ellipse(mouseX,mouseY,10+8*n,10+8*n);
//  }

fill(180,200,255);
    ellipse(mouseX,mouseY,100,100);

  t += 1;
}

