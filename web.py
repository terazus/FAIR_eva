from flask import Flask, render_template, request, jsonify
import requests
import time
from bs4 import BeautifulSoup
from flask_wtf import FlaskForm
from wtforms import SelectField, TextField, validators
import json

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'sdafasfwefq3egthyjtyhwef',
    'TESTING': True,
    'DEBUG': True,
    'FLASK_DEBUG': 1
    })

@app.route('/')
def index():
    form = CheckIDForm(request.form)
    return render_template('index.html', form=form)

@app.route('/evaluator', methods=['GET', 'POST'])
def evaluator():
  try:
    args = request.args
    form = CheckIDForm(request.form)
    item_id = args['item_id']
    repo = args['repo']

    result_points = 0
    num_of_tests = 41

    findable = {}
    accessible = {}
    interoperable = {}
    reusable = {}
    body = json.dumps({'id': item_id, 'repo': repo})
  except Exception as e:
    print("Problem creating the object")
    print(e)

  url = 'http://localhost:9090/v1.0/rda/all'
  result = requests.post(url, data = body, headers={'Content-Type': 'application/json'})
  print(result.json()) 
  return render_template('eval.html', item_id=item_id,
          findable=result.json()['findable'], 
          accessible=result.json()['accessible'],
          interoperable=result.json()['interoperable'],
          reusable=result.json()['reusable'],
          result_points=result_points)

class CheckIDForm(FlaskForm):
    item_id = TextField(u'ITEM ID','')
    repo = TextField(u'REPO','')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
