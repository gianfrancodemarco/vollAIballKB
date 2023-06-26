import os
import sys
import debugpy

module_path = os.path.abspath(os.path.dirname(__file__))
print(module_path)
sys.path.append(module_path)

# standard
from flask import Flask, request, jsonify, Response
from logger import *
from pyswip import Prolog

app = Flask(__name__)

knowledgeBase = Prolog()
knowledgeBase.dynamic("scored/1")
knowledgeBase.assertz("""narrative(score, Text) :- format(atom(Text), "Total score: ~w : ~w.", [score(1), score(0)])""")
knowledgeBase.assertz("""narrative(scored, Text) :- scored(Player), format(atom(Text), "~w scored.", [Player])""")
knowledgeBase.assertz("""all_narratives(Narratives) :- findall(Text, narrative(_, Text), Narratives)""")

debugpy.listen(("0.0.0.0", 5678))

logging.info(f'Started flask app: {__name__}')

# NOTE: IMPORTANT!
# Add every new predicate here
PREDICATES = [
    'team(X)',
    'player(X,Y)',
    'touchPlayerAtAction(X,Y,W,Z)',
    'touchPlayerAtAction(X,X,W,Z)',
    'hitOutOfBounds(X,Y,Z)',
    'hitGoal(X,Y,Z)',
    'hitIntoBlueArea(X,Y,Z)',
    'hitIntoRedArea(X,Y,Z)',
    'hitWall(X,Y,Z)'
]

QUERY = {
    'nice_action':'touchPlayerAtAction(_, <episode_name>, _, 2).',
    'last_episode': 'touchPlayerAtAction(_, Episode, _, _), \+ (touchPlayerAtAction(_, Episode2, _, _), Episode2 > Episode).'
}


@app.route('/', methods=['GET'])
def health() -> Response:
    return jsonify({'status': 'OK'})

@app.route('/reset', methods=['POST'])
def retractall() -> Response:
    logging.warning(f'Resetting knowledge base')
    for predicate in PREDICATES:
        knowledgeBase.retractall(predicate)
    return jsonify({'status': 'OK'})

@app.route('/assert', methods=['POST'])
def assertz() -> Response:
    logging.info(f'Asserting fact: {request.json["fact"]}')
    fact = request.json['fact']
    knowledgeBase.assertz(fact)
    return jsonify({'status': 'OK'})

@app.route('/query', methods=['POST'])
def queryz() -> Response:
    logging.info(f'Querying: {request.json["query"]}')
    query = request.json['query']
    result = list(knowledgeBase.query(query))
    logging.info(f'Response: {result}')
    return jsonify({'status': 'OK', 'response': result})

@app.route('/narrative', methods=['POST'])
def narrative() -> Response:
    file_path = "narrative.txt"
    query = request.json['query']
    results = list(knowledgeBase.query(f"all_narratives(Narratives)"))
    results = [result["Narratives"] for result in results] 
    return jsonify({'status': 'OK', 'response': results})

# find -O3 -L . -name "*.txt"