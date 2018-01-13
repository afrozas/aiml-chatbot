from flask import Flask

import aiml, os

app = Flask(__name__)


@app.route('/')
def index():
	return 'Index Page'


@app.route('/computers/<string:user_text>')
def computers(user_text):
	pass


def spinKernel():
	kernel = aiml.Kernel()
	kernel.learn("knowledge/computers.aiml")
	while True:
		print(kernel.respond(input("Enter your message >> ")))


if __name__ == '__main__':
	spinKernel()
	app.run()
