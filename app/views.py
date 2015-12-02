#!/usr/bin/env python

import flask, flask.views
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify
import json
import os
import json
import requests

from app import app

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

users = {
    "john": "hello",
    "spongebob":"squarepants"
}

def get_dict(**kwargs):
    d= {}
    for k,v in kwargs.iteritems():
        d[k] = v
    return d


@app.route('/')
def home():
    #select * from salesforce
    with open("%s/data_dump.json"%DIR_PATH, "rb") as f:
        data=json.loads(f.read())
    
    data_rows=[
        ['Elon Musk','elon.musk@musk.com','918447789937','100'],
        ['Elon Musk','elon.musk@musk.com','918447789937','100']
    ]
    return flask.render_template('index.html',data_rows=data_rows,data=data)


@app.route('/user/<user_id>')
def viewBlog(user_id):
    #make query to salesforce account
    with open("%s/data_dump.json"%DIR_PATH, "rb") as f:
        data=json.loads(f.read())

    record =''
    for i in data:
        if i[0][-2] == user_id:
            record = i
    
    return flask.render_template('userprofile.html',record=record)



@app.route('/api/<user_id>')
def morning(user_id):
    #make query to salesforce account
    with open("%s/data_dump.json"%DIR_PATH, "rb") as f:
        data=json.loads(f.read())

    if user_id == 'all':
        return jsonify(data=data)

    record =''
    for i in data:
        if i[0][-2] == user_id:
            record = i
    
    return jsonify(data=record)


def push(data_dict):
    access_token = util.get_access_token()['access_token']
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-type': 'application/json'}

    url = '/services/data/v34.0/sobjects/foo__c/'

    new_account = data_dict
    json_new_account = json.dumps(new_account)

    conn = util.get_connection()
    conn.request("POST", url, json_new_account, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(json.loads(data))
    print(data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')



