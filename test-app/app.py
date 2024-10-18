from flask import Flask
import os

app = Flask(__name__)

@app.route('/load/<int:workers>')
def load(workers):
	os.system("stress --cpu {workers} --timeout 10")
	return "CPU load with {workers} workers started."

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

