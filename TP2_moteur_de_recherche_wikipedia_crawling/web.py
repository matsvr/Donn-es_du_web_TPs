#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, make_response
import sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode, unquote
from datetime import datetime
import uuid
from query import getResults

app = Flask(__name__)
app.secret_key = "NOT_SO_SECRET"


def countPages():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM webpages")
        res = cur.fetchone()
        print (res)
        return res[0]

@app.route('/', methods=['GET'])
def index():
    return make_response(render_template('index.html'))

@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    if q:
        results = getResults(q)
        processed_results = []
        for r in results:
            result = {}
            result['url'] = r[0]
            result['title'] = r[1]
            soup = BeautifulSoup(r[2], "html.parser")
            infobox = soup.find('div', class_='infobox_v3') 
            if infobox:
                img = infobox.find('img')
                if img:
                    src = img['src']
                    if src:
                        result['img'] = urljoin(result['url'], src)
            processed_results.append(result)
        resp = make_response(render_template('results.html', q=q, results=processed_results))
        return resp
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8080)

