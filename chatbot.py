from flask import Flask, request, render_template
import aiml
import os
import requests
import json
import datetime
from time import sleep
import gc
import pandas as pd
# from dbconnect import connection

app = Flask(__name__)

atomic_kernel = None
cities = []


def weather_parser(response, place):
    """
    """
    if response is None:
        resp = json.load(open("templates/weath.er"))
    else:
        resp = json.loads(response)
    # print(resp)
    current = resp['currently']
    summary = resp['hourly']['summary']
    statement = 'It is going to be ' + str(summary.lower()) + ' The temperature is ' + str(current['temperature']) + ' degrees F, humidity ' + str(
        current['humidity']) + ', wind speed is ' + str(current['windSpeed']) + ' kmph with a visibility of ' + str(current['visibility']) + ' kilometres.'
    return statement


def weather(place):
    # set your API key from api.darksky.net as environment variable 
    API_KEY = os.environ['API_KEY']
    url = "https://api.darksky.net/forecast/" + API_KEY + '/' + \
        place
    forecast = requests.get(url)
    return weather_parser(forecast.text, place)


@app.route('/')
def index():
    global atomic_kernel
    atomic_kernel = spin_kernel('atomic')
    
    global cities
    cities = pd.read_csv(r'weather/city.csv')
    cities.drop(
        ['locId', 'country', 'region', 'postalCode', 'metroCode', 'areaCode'],
        inplace=True, axis=1)
    # print(cities)
    # cities.sort_values(by='city', ascending=False).groupby(level=0).first()
    return render_template('index.html')
    # return "Hi, this is AI Bot. Make a request to /<message> to get started."


@app.route('/respond/<string:user_text>')
def atomic_router(user_text, methods=['GET']):
    lower_text = user_text.lower()

    if lower_text.find('weather') > -1 or lower_text.find('temperature') > -1:
        words = lower_text.split()
        for word in words:
            print(word)
            word = word.title()
            row = cities.loc[cities['city'] == word]
            if(row.size > 0):
                place = str(row['latitude'].values[0]) + ',' + str(row['longitude'].values[0])
                response = weather(place)
            else:
                response = "Did you forget to tell me the city?"
    else:
        response = atomic_kernel.respond(user_text.upper())
    sleep(len(response) * 0.01 + 1)

    # c, conn = connection()
    # c.execute("INSERT INTO chat_logs (msg_user,msg_bot,timestramp) VALUES(%s,%s,%s);",
    #         ((user_text),(response), str(datetime.datetime.now())))
    # conn.commit()
    # c.close()
    # conn.close()
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
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port, debug=True)
