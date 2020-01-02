from flask import Flask
from flask import json
from flask import request
from flask import Response
import sqlite3


DATABASE_NAME = "hero_database.db"


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    content = open("index.html").read()
    return Response(content, mimetype="text/html")


@app.route("/all_heroes", methods=["GET"])
def all_heroes():
    all_heroes_query = """SELECT * FROM HEROES"""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(all_heroes_query)
    conn.commit()

    data = {"heroes": [{"id": a, "name": b, "primary_attr": c} for a, b, c, _, _ in cursor]}
    js = json.dumps(data)

    cursor.close()
    conn.close()

    return Response(js, status=200, mimetype='application/json')


@app.route("/good_with", methods = ["POST"])
def good_with():
    data_json = json.loads(request.data)
    hero_id = data_json["id"]

    good_with_query = """
        SELECT hero_id_1 as h
        FROM SYNERGY_WITH
        WHERE hero_id_2 = {}

        UNION

        SELECT hero_id_2 as h
        FROM SYNERGY_WITH
        WHERE hero_id_1 = {}
    """

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(good_with_query.format(hero_id, hero_id))
    conn.commit()

    data = {"good_with": [a[0] for a in cursor]}
    js = json.dumps(data)

    cursor.close()
    conn.close()

    return Response(js, status=200, mimetype='application/json')


@app.route("/good_against", methods = ["POST"])
def good_against():
    data_json = json.loads(request.data)
    hero_id = data_json["id"]

    good_against_query = """
        SELECT hero_id_2 as h
        FROM SYNERGY_AGAINST
        WHERE hero_id_1 = {}
    """

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(good_against_query.format(hero_id))
    conn.commit()

    data = {"good_against": [a[0] for a in cursor]}
    js = json.dumps(data)

    cursor.close()
    conn.close()

    return Response(js, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
