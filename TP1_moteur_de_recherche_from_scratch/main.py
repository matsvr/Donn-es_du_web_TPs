#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from bs4 import BeautifulSoup
import requests
import sqlite3
from urllib.parse import urljoin

app = Flask(__name__)
app.secret_key = "TODO: mettre une valeur secrète ici"


def countPages():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM webpages")
        res = cur.fetchone()
        print(res)
        return res[0]


def getResults(query):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT URL, title, content FROM webpages"
                    + " WHERE title LIKE ? LIMIT 10",
                    ('%' + query + '%',))
        results = cur.fetchall()
        final_results = []
        for result in results:
            result = list(result)
            result.append(getImages(result[0], result[2]))
            final_results.append(result)

        return final_results


def getImages(url, content):
    soup = BeautifulSoup(content, 'html.parser')
    obj = soup.find('div', class_='infobox_v3')
    if obj:
        image = obj.find('div', class_='images')
        if image:
            img = image.find('img')
            if img:
                image_url = img.get('src')
                # code en dessous avec aide externe
                absolute_image_URL = urljoin(url, image_url)
                image_url = absolute_image_URL
            else:
                image_url = None
        else:
            image_url = None
    else:
        image_url = None
    return image_url


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', count=countPages())


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    results = getResults(query)
    return render_template('results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
