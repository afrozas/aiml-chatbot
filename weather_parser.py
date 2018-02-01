import json
def weather_parser(response):
	"""
	"""
	resp = json.load(open("templates/weath.er"))
	current = resp['currently']
	summary = resp['hourly']['summary']
	statement = 'It is going to be ' + str(summary.lower()) + ' The temperature is ' + str(current['temperature'])  + ' degrees F, humidity ' + str(current['humidity']) + ', wind speed is ' + str(current['windSpeed']) + ' kmph with a visibility of ' + str(current['visibility']) + ' kilometres.'
	print(statement)



if __name__ == '__main__':
	weather_parser(None)