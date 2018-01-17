from flask import Flask, request, render_template

import aiml, os, requests

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')
	# return "Hi, this is AI Bot. Make a request to /<message> to get started."


@app.route('/<string:user_text>')
def atomic_router(user_text, methods=['GET']):
	atomic_kernel = spin_kernel('atomic')
	response = atomic_kernel.respond(user_text.upper())
	return response	


@app.route('/weather/<place>')
def weather(place, methods=['GET']):
	place = "17.3850,78.4867"
	url = "https://api.darksky.net/forecast/f0a1f30256be08ae33bc0f9c27ad67fb/" + place
	forecast = requests.get(url)
	return forecast.text


@app.route('/computers/<string:user_text>')
def computers(user_text, methods=['GET']):
	computers_kernel = spin_kernel('computers')
	response = computers_kernel.respond(user_text.upper())
	return response


@app.route('/eateries/<string:user_text>')
def eateries(user_text, methods=['GET']):
	eateries_kernel = spin_kernel('eateries')
	response = eateries_kernel.respond(user_text.upper())
	return response


def spin_kernel(knowledge_file):
	""" 
	method to spin an AIML Kernel from knowledge file
	args: knowledge_file, placed inside 'knowledge/' folder
		  file name only required, path and extension is self appended
		  argument 'computers' will be read as => 'knowledge/computers.aiml'
	returns: kernel, learned from knowledge_file
	"""
	kernel = aiml.Kernel()
	green_aimls = get_all_files('green')
	for aiml_file in green_aimls:
		kernel.learn(aiml_file)
	return kernel


def get_all_files(color):
	"""
	List all files recursively in the root specified by root
	"""
	files_list = []
	root = 'knowledge/' + color
	for path, subdirs, files in os.walk(root):
	    for name in files:
	    	files_list.append(os.path.join(root, name))
	print(files_list)
	return files_list[0:-1]

if __name__ == '__main__':
	app.run(debug=True)
