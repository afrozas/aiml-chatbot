from flask import Flask, request, render_template
import aiml, os, requests, json
import datetime
from time import sleep
import gc
from dbconnect import connection

app = Flask(__name__)

atomic_kernel = None

def weather_parser(response,place):
	"""
	"""
	if response is None:
		resp = json.load(open("templates/weath.er"))
	else:
		resp = json.loads(response)
	print(resp)
	current = resp['currently']
	summary = resp['hourly']['summary']
	statement = 'It is going to be ' + str(summary.lower()) + ' The temperature is ' + str(current['temperature'])  + ' degrees F, humidity ' + str(current['humidity']) + ', wind speed is ' + str(current['windSpeed']) + ' kmph with a visibility of ' + str(current['visibility']) + ' kilometres.'
	return statement

def weather(place):
	place = "17.3850,78.4867"
	url = "https://api.darksky.net/forecast/f0a1f30256be08ae33bc0f9c27ad67fb/" + place
	forecast = requests.get(url)
	return weather_parser(forecast.text,place)


@app.route('/')
def index():
	global atomic_kernel
	atomic_kernel= spin_kernel('atomic')
	return render_template('index.html')
	# return "Hi, this is AI Bot. Make a request to /<message> to get started."


@app.route('/respond/<string:user_text>')
def atomic_router(user_text, methods=['GET']):
	lower_text = user_text.lower()

	if lower_text.find('weather') > -1 or lower_text.find('temperature') > -1:
		response = weather(None)
	else:
		response = atomic_kernel.respond(user_text.upper())
		sleep(len(response)*0.03+1)

	c, conn = connection()
	c.execute("INSERT INTO chat_logs (msg_user,msg_bot,timestramp) VALUES(%s,%s,%s);",
	 		  ((user_text),(response), str(datetime.datetime.now())))
	conn.commit()
	c.close()
	conn.close()
	gc.collect()
	return response	


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
