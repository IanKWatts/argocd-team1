from flask import Flask
import os

app = Flask(__name__)

@app.route('/load/<int:workers>')
def load(workers):
	os.system(f"stress --cpu {workers} --timeout 10")
	return f"CPU load with {workers} workers started.\n"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

