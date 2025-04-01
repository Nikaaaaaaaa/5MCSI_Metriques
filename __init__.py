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

@app.route("/commits/")
def commits():
    url = "https://api.github.com/repos/Nikaaaaaaaa/5MCSI_Metriques/commits"
    response = urlopen(url)
    raw_data = response.read().decode("utf-8")
    json_data = json.loads(raw_data)

    compteur = {}

    for commit in json_data:
        date_str = commit["commit"]["author"]["date"]
        minute = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").minute
        compteur[minute] = compteur.get(minute, 0) + 1

    result = [{"minute": k, "commits": v} for k, v in sorted(compteur.items())]
    return jsonify(results=result)
  
@app.route('/commits-view/')
def commits_view():
    return render_template("commits.html")

  
if __name__ == "__main__":
  app.run(debug=True)
