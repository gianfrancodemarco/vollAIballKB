import os
import sys
import debugpy

module_path = os.path.abspath(os.path.dirname(__file__))
print(module_path)
sys.path.append(module_path)

# standard
from flask import Flask, request, jsonify, Response
from logger import *
from knowledge_base import knowledge_base

app = Flask(__name__)

debugpy.listen(("0.0.0.0", 5678))

logging.info(f'Started flask app: {__name__}')

# NOTE: IMPORTANT!
# Add every new predicate here
# This should be completed with every combination when 2 or more variables
# can share a value
PREDICATES = [
    'team(X)',
    'player(X)',
    'playsinteam(X,Y)',
    'touchplayerataction(X,Y,W,Z)',
    'hitoutofbounds(X,Y,Z)',
    'hitbluegoal(X,Y,Z)',
    'hitredgoal(X,Y,Z)',
    'hitintobluearea(X,Y,Z)',
    'hitintoredarea(X,Y,Z)',
    'hitwall(X,Y,Z)'
]

@app.route('/', methods=['GET'])
def health() -> Response:
    return jsonify({'status': 'OK'})

@app.route('/reset', methods=['POST'])
def retractall() -> Response:
    logging.warning(f'Resetting knowledge base')
    for predicate in PREDICATES:
        knowledge_base.retractall(predicate)
    return jsonify({'status': 'OK'})

@app.route('/assert', methods=['POST'])
def assertz() -> Response:
    logging.info(f'Asserting fact: {request.json["fact"]}')
    fact = request.json['fact'].lower()
    logging.info("Asserting: " + fact)
    knowledge_base.assertz(fact)
    return jsonify({'status': 'OK'})

@app.route('/query', methods=['POST'])
def queryz() -> Response:
    logging.info(f'Querying: {request.json["query"]}')
    query = request.json['query']
    result = list(knowledge_base.query(query))
    logging.info(f'Response: {result}')
    return jsonify({'status': 'OK', 'response': result})

@app.route('/narrative', methods=['GET'])
def narrative() -> Response:
    results = list(knowledge_base.query(f"all_narratives(Narratives)"))
    return jsonify({'status': 'OK', 'response': results[0]["Narratives"]})

# find -O3 -L . -name "*.txt"