from flask import Flask, render_template, request
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
                    print text
                    self.anim.setColour(text,noise=3.0)
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
		timeString = now.strftime("%Y-%m-%d %H:%M:%S")
		templateData = {
		  'time': timeString
		  }
		return render_template('main.html', **templateData)

	@app.route('/change_colour', methods=['POST'])
	def handle_data():
		cHex = request.form['newcolour']
		cInt = [int(cHex[0:2],16),
					int(cHex[2:4],16),
					int(cHex[4:6],16)]
		queue.put(cInt)
		now = datetime.datetime.now()
		timeString = now.strftime("%Y-%m-%d %H:%M:%S")
		templateData = {
		  'time': timeString
		  }
		return render_template('main.html', **templateData)
		
	return app

if __name__ == "__main__":
	
	app = create_app()	
	app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)

