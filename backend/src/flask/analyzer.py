#!/usr/bin/python3 -B
# analyzer.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import psycopg2
from threading import Thread
from web.twitter import get_tweets
from flask import Blueprint, request, jsonify
from config import DB_NAME, DB_USER, DB_PASSWORD


analyzer_blueprint = Blueprint('analyzer_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# New user submission
@analyzer_blueprint.route('/people/new/', methods=['POST'])
def post_new_person():
    if not request.is_json:
        return 'Invalid JSON request', 400
    username = request.get_json()['handle'].replace('@', '', 1)
    thread = Thread(target=analyze_person, args=(username,))
    thread.start()
    return 'Success', 200


def analyze_person(username):
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    cursor.execute('''
DELETE FROM person
      WHERE username = %s;
''', (username,))
    conn.commit()

    name, picture, tweets = get_tweets(username, 100, True)

    cursor.execute('''
INSERT INTO person
            (
                username,
                name,
                picture
            )
     VALUES (
                %s,
                %s,
                %s
            );
''', (username, name, picture))

    params = []
    for tweet in tweets:
        params.append(username)
        params.append(tweet)

    cursor.execute('''
INSERT INTO tweet
            (
                username,
                tweet
            )
     VALUES ''' + ', '.join(['(%s, %s)'] * len(tweets)) + ';', tuple(params))
    conn.commit()
    conn.close()