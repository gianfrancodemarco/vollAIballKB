import os
import sys

module_path = os.path.abspath(os.path.dirname(__file__))
print(module_path)
sys.path.append(module_path)

# standard
from flask import Flask, request, jsonify, Response
from logger import *
from knowledge_base import KnowledgeBase

app = Flask(__name__)
knowledgeBase = KnowledgeBase()

knowledgeBase.assertz('acted("Miracle at St. Anna", "Michael DenDekker")')
knowledgeBase.assertz('acted("Miracle at St. Anna", "sad")')
for a in knowledgeBase.query('acted("Miracle at St. Anna", X)'):
    print(a)




logging.info(f'Started flask app: {__name__}')

@app.route('/', methods=['GET'])
def health() -> Response:
    return jsonify({'status': 'OK'})

@app.route('/assert', methods=['POST'])
def assertz() -> Response:
    logging.info(f'Asserting fact: {request.json["fact"]}')
    fact = request.json['fact']
    knowledgeBase.assertz(fact)
    return jsonify({'status': 'OK'})

@app.route('/query', methods=['POST'])
def query() -> Response:
    logging.info(f'Querying: {request.json["query"]}')
    query = request.json['query']
    response = knowledgeBase.query(query)
    logging.info(f'Response: {list(response)}')
    return jsonify({'status': 'OK', 'response': list(response)})
