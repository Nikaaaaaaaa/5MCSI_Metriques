from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def page_contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': round(temp_day_value, 2)})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

import requests
from collections import Counter
from flask import jsonify
from datetime import datetime

@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/Nikaaaaaaaa/5MCSI_Metriques/commits'
    response = requests.get(url)
    commit_data = response.json()

    minute_counts = Counter()

    for commit in commit_data:
        date_str = commit.get('commit', {}).get('author', {}).get('date')
        if date_str:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = dt.minute
            minute_counts[minute] += 1

    results = [{'minute': m, 'commits': c} for m, c in sorted(minute_counts.items())]
    return jsonify(results=results)


  
@app.route('/commits-view/')
def commits_view():
    return render_template("commits.html")

  
if __name__ == "__main__":
  app.run(debug=True)
