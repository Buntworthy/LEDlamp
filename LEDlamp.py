import opc
import time
import random
import math
from pnoise import raw_noise_2d
from pnoise import raw_noise_3d

class BaseAnimation():
        """ Class to handle animation of a single colour for all LEDs,
        and animation between colours
        """

        def __init__(self, nLEDs):
                """ Create the list of Pixel objects """
                # Specify the number of leds
                self.nLEDs = nLEDs
                self.dimensions = False
                self.time = 0

                # Each pixel is an object
                self.pixels = []
                for LED in range(self.nLEDs):
                        self.pixels.append(Pixel())

        def setDimensions(self, w, h):
                """ Set dimension for spatially noisy transitions"""
                self.dimensions = True
                self.w = w
                self.h = h

        def update(self, dt):
                """ Update all the pixels objects """
                self.time += dt
                for pix in self.pixels:
                        pix.update(dt)

        def render(self):
                """ Get and return the colour for each pixel"""
                colours = []
                for pix in self.pixels:
                        colours.append(pix.getColour())

                return colours

class ColourAnimation(BaseAnimation):
        
        def setNoise(self, noiseFreq, noiseAmp):
                """ Add Perlin noise to the pixels """
                for pix in self.pixels:
                        pix.setNoise(noiseFreq,noiseAmp)

        def setColour(self, c, noise=0.0):
                """ Change the colour of all the pixels to a target colour
                Noise defines the time in seconds over which the transition can occur
                """
                print('Setting colours to ' + str(c))
                if self.dimensions:
                        for idx, pix in enumerate(self.pixels):
                                pix.setC(c, noise*(0.5 + 0.5*raw_noise_3d( self.time, 0.1*idx%self.w , 0.1*math.floor(idx/self.h) )))
                else:
                        for pix in self.pixels:
                                pix.setC(c, noise*random.random())

class Pixel():
        """ Class to handle the behaviour of a single pixel"""

        # Static state variables
        STATE_STATIC = 0
        STATE_CHANGING = 1

        def __init__(self):
                """ Initialise the pixel to off """
                self.c = [0,0,0]                # Current colour
                self.targetC = [0,0,0]          # Target colour when interpolating
                self.origC = [0,0,0]            # Record of original colour when interpolating
                self.dt = 0.0                   # Interpolation time
                self.state = Pixel.STATE_STATIC # Current state of the pixel
                self.time = time.time()         # Pixel internal clock
                self.noiseFreq = 0              # Frequency of Perlin noise
                self.noiseOffset = 0            # Offset of Perlin noise
                self.noise = False              # If we should apply colour noise

        def setC(self, newC, dt=0.0):
                """ Method to change the colour of the pixel 
                to colour newC, over time dt
                """

                if dt>0:
                        self.origC = self.c[:]                  # Record the original colour
                        self.targetC = newC[:]                  # Set the target
                        self.timeStart = self.time              # Time at which colour change starts
                        self.timeEnd = self.time + dt           # Time at which colour change ends 
                        self.state = Pixel.STATE_CHANGING       # Change state
                else:
                        self.c = newC[:]

        def update(self, dt):
                """ Update the Pixel"""

                # Increment the internal clock
                self.time += dt

                if self.state is Pixel.STATE_CHANGING:

                        # Interpolate toward the target colour
                        timeLeft = float(self.timeEnd - self.time)
                        totalTime = float(self.timeEnd - self.timeStart)
                        
                        # Check how much time is left in the interpolation
                        if timeLeft > 0 and totalTime != 0:
                                blendFraction = timeLeft/totalTime
                        
                                self.c[0] = int(blendFraction*self.origC[0] + (1 - blendFraction)*self.targetC[0])
                                self.c[1] = int(blendFraction*self.origC[1] + (1 - blendFraction)*self.targetC[1])
                                self.c[2] = int(blendFraction*self.origC[2] + (1 - blendFraction)*self.targetC[2])

                        else:
                                self.c = self.targetC[:]
                                self.state = Pixel.STATE_STATIC
        
        def getColour(self):
                """ Returns the current colour of the pixel """

                if self.noise:

                        # Add Perlin noise to the current Pixel colour
                        returnC = [0,0,0]
                        returnC[0] = int(self.c[0]*(1 + self.noiseAmp*raw_noise_2d(  0, self.noiseOffset + self.time*self.noiseFreq)))
                        returnC[1] = int(self.c[1]*(1 + self.noiseAmp*raw_noise_2d(100, self.noiseOffset + self.time*self.noiseFreq)))
                        returnC[2] = int(self.c[2]*(1 + self.noiseAmp*raw_noise_2d(200, self.noiseOffset + self.time*self.noiseFreq)))

                        # cap the values
                        # TODO make this a utility function
                        returnC[0] = max( min(returnC[0],255), 0 )
                        returnC[1] = max( min(returnC[1],255), 0 )
                        returnC[2] = max( min(returnC[2],255), 0 )

                else:
                        returnC = self.c[:]

                return returnC

        def setNoise(self,noiseFreq, noiseAmp):
                """ Enables noise on the Pixel colour """

                self.noiseFreq = noiseFreq
                # Ensure that different pixels are at different points on the noise profile
                self.noiseOffset = 1000*random.random()
                self.noiseAmp = noiseAmp
                self.noise = True

if __name__ == '__main__':
        
        # Set up the opc client
        client = opc.Client('localhost:7890')

        # Set up a colour animation and set an initial colour
        anim = ColourAnimation(60)
        anim.setColour([100,50,30],0.0)
        anim.setDimensions(10,6)
        anim.setNoise(1, 0.05)

        # Run the animation, and randomly change colour
        while True:

                anim.update(0.1)
                pixels = anim.render()
                client.put_pixels(pixels)
                time.sleep(0.1)

                if random.random() < 0.03:
                        # Change the colours of the pixels (over the course of 1s)
                        anim.setColour([random.randint(0,255),
                                                random.randint(0,255),
                                                random.randint(0,255)],noise=3.0)
