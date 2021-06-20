from __future__ import print_function

import time

import os.path as path
import sys

root = path.join(path.dirname(path.realpath(__file__)), "..")
sys.path.append(root)

import six
from flask import Flask, jsonify, render_template, request
import json
from pymongo import MongoClient
from components.standalone_parser import StandaloneParser

app = Flask(__name__)
parsers = dict()
client = MongoClient()

@app.route("/")
def default():
    return render_template('default.html')


@app.route('/parse/<dataset>', methods=['GET'])
def parse(dataset):
    utterance = request.args['q']

    parser = parsers[dataset]

    if six.PY2:
        utterance = utterance.encode('utf-8', 'ignore')

    hypotheses = parser.parse(utterance, debug=True)

    responses = dict()
    responses['hypotheses'] = []

    for hyp_id, hyp in enumerate(hypotheses):
        print('------------------ Hypothesis %d ------------------' % hyp_id)
        print(hyp.code)
        print(hyp.tree.to_string())
        print(hyp.score.item())
        print(hyp.rerank_score.item())

        # print('Actions:')
        # for action_t in hyp.action_infos:
        #     print(action_t)

        actions_repr = [action.__repr__(True) for action in hyp.action_infos]

        hyp_entry = dict(id=hyp_id + 1,
                         value=hyp.code,
                         tree_repr=hyp.tree.to_string(),
                         score=hyp.rerank_score.item() if hasattr(hyp, 'rerank_score') else hyp.score.item(),
                         actions=actions_repr)

        responses['hypotheses'].append(hyp_entry)

    return jsonify(responses)


@app.route("/upload", methods=['POST'])
def upload():
    try:
        req_data = request.get_json()
        db = client['tranx']
        collection = db['events']
        req_data['timestamp'] = int(time.time())
        collection.insert_one(req_data)
        return "success"
    except Exception as e:
        print(e)
        return "failed"


@app.route("/run", methods=['POST'])
def run():
    input = request.get_json()["code"]
    hypotheses = parsers["natural"].parse(input)
    output = hypotheses[0].code
    # TODO: make this safe !important
    return str(eval(output))


config_dict = json.load(open(path.join(root, 'config', 'server', 'config_py3.json')))
for parser_id, config in config_dict.items():
    parser = StandaloneParser(parser_name=config['parser'],
                              model_path=config['model_path'],
                              example_processor_name=config['example_processor'],
                              beam_size=config['beam_size'],
                              reranker_path=config['reranker_path'],
                              cuda=False)

    parsers[parser_id] = parser

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
