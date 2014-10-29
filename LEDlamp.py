import opc
import time
import random
from pnoise import raw_noise_2d

class GradientAnimation():

        def __init__(self, nLEDs):
                
                # Specify the number of leds
                self.nLEDs = nLEDs

                # Each pixel is an object
                self.pixels = []
                for LED in range(self.nLEDs):
                        self.pixels.append(Pixel())

                for pix in self.pixels:
                        pix.setNoise(0.5,0.1)

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
                        colours.append(pix.getColour())

                return colours

class Pixel():

        stateStatic = 0
        stateChanging = 1

        def __init__(self):

                # Set the default colour to black
                self.c = [0,0,0]
                self.targetC = [0,0,0]  # When interpolating
                self.origC = [0,0,0]    # When interpolating
                self.dt = 0.0           # Interpolation time
                self.state = Pixel.stateStatic
                self.time = time.time()
                self.noiseFreq = 0
                self.noiseOffset = 0
                self.noise = False      # If we should apply colour noise

        def setC(self, newC, dt=0.0):

                if dt>0:
                        self.origC = self.c[:]
                        self.targetC = newC[:]
                        self.timeStart = self.time # Time at which c change starts
                        self.timeEnd = self.time + dt # Time at which c change ends 
                        self.state = Pixel.stateChanging
                else:
                        self.c = newC[:]

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
                                self.c = self.targetC[:]
                                self.state = Pixel.stateStatic
        
        def getColour(self):
                # Method to get the current colour of the pixel
                if self.noise:
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
                self.noiseFreq = noiseFreq
                self.noiseOffset = 1000*random.random()
                self.noiseAmp = noiseAmp
                self.noise = True

if __name__ == '__main__':
        
        client = opc.Client('localhost:7890')

        anim = GradientAnimation(60)
        anim.setColour([100,50,30],0.0)

        while True:

                anim.update(0.1)
                pixels = anim.render()
                client.put_pixels(pixels)
                time.sleep(0.1)

                if random.random() < 0.05:
                        # Change the colours of the pixels (over the course of 1s)
                        anim.setColour([random.randint(0,100),
                                                        random.randint(0,100),
                                                        random.randint(0,100)],noise=1.0)
