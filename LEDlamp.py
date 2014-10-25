import opc
import time
import random
#from noise import pnoise1

class GradientAnimation():

        def __init__(self, nLEDs):
                
                # Specify the number of leds
                self.nLEDs = nLEDs

                # Each pixel is an object
                self.pixels = []
                for LED in range(self.nLEDs):
                        self.pixels.append(Pixel())

        def setColour(self, c, noise=0.0):
                # Change the colour of all the pixels with a temporal noise
                print('Setting colours to ' + str(c))
                for pix in self.pixels:
                        pix.setC(c, noise*random.random())

        def update(self, dt):
                for pix in self.pixels:
                        pix.update(dt)

        def render(self):

                colours = []
                for pix in self.pixels:
                        colours.append(pix.c)

                return colours

class Pixel():

        stateStatic = 0
        stateChanging = 1

        def __init__(self):

                # Set the default colour to black
                self.c = [0,0,0]
                self.targetC = [0,0,0]
                self.dt = 0.0
                self.state = Pixel.stateStatic
                self.time = time.time()

        def setC(self, newC, dt=0.0):
                self.origC = self.c
                self.targetC = newC
                self.timeStart = self.time # Time at which c change starts
                self.timeEnd = self.time + dt # Time at which c change ends 
                self.state = Pixel.stateChanging

        def update(self, dt):

                self.time += dt

                if self.state is Pixel.stateChanging:
                        
                        # Interpolate toward the target colour
                        timeLeft = float(self.timeEnd - self.time)
                        totalTime = float(self.timeEnd - self.timeStart)
                        
                        if timeLeft > 0 and totalTime != 0:
                                blendFraction = timeLeft/totalTime
                        
                                self.c[0] = int(blendFraction*self.origC[0] + (1 - blendFraction)*self.targetC[0])
                                self.c[1] = int(blendFraction*self.origC[1] + (1 - blendFraction)*self.targetC[1])
                                self.c[2] = int(blendFraction*self.origC[2] + (1 - blendFraction)*self.targetC[2])

                        else:
                                self.state = Pixel.stateStatic

        def addNoise(self):
                pass

if __name__ == '__main__':
        
        client = opc.Client('localhost:7890')

        anim = GradientAnimation(60)
        anim.setColour([100,50,30],1.0)

        while True:

                anim.update(0.1)
                pixels = anim.render()
                client.put_pixels(pixels)
                time.sleep(0.1)

                if random.random() < 0.01:
                        # Change the colours of the pixels (over the course of 1s)
                        anim.setColour([random.randint(0,100),
                                                        random.randint(0,100),
                                                        random.randint(0,100)],noise=20.0)
