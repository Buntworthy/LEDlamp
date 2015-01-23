from flask import Flask, render_template
import datetime
import threading
import time
import Queue
from lampAnimation import *


queue = Queue.Queue()

class ThreadClass(threading.Thread):

    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.counter = 0

    def run(self):
        print 'running lamp thread'
        # Set up the opc client
        self.client = opc.Client('localhost:7890')

        # Set up a colour animation and set an initial colour
        self.anim = ColourAnimation(60)
        self.anim.setColour([100,50,30],0.0)
        self.anim.setDimensions(10,6)
        self.anim.setNoise(1, 0.05)

        # Run the animation, and randomly change colour
        while True:

            self.anim.update(0.1)
            self.pixels = self.anim.render()
            self.client.put_pixels(self.pixels)
            time.sleep(0.1)
            # Check for a new colour in the queue
            try:
                text = self.queue.get(False)
                if len(text) > 0:
                    #print "changing colour"
					self.anim.setColour([random.randint(0,255),random.randint(0,255),random.randint(0,255)],noise=3.0)
            except:
                pass

def create_app():
	app = Flask(__name__)
	t = ThreadClass(queue)
	t.setDaemon(True)
	t.start()

	@app.route("/")
	def hello():
		now = datetime.datetime.now()
		timeString = now.strftime("%Y-%m-%d %H:%M")
		templateData = {
		  'title' : 'HELLO!',
		  'time': timeString
		  }
		return render_template('main.html', **templateData)


	@app.route("/something/")
	def something():
		queue.put('message!')
		print('I sent a message\n')
		templateData = {
		  'title' : 'HELLO!',
		  'time': 'wut?'
		  }
		return render_template('main.html', **templateData)

	return app

if __name__ == "__main__":
	
	app = create_app()	
	app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)

