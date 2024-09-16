#!/usr/bin/env python3

import sqlite3
import re
from math import log
from shared import extractText, stem
from collections import defaultdict


def getResults(query):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    queryWords = [stem(w) for w in query.split()]


    pagerank = dict() # contient le page-rank de chaque document
    tfidf = defaultdict(float) # contient le tf-idf de chaque document
    
    # étape 1 : remplir le dictionnaire tf-idf 
                
    # étape 2 : remplir le page rank


    # étape 3 : calcul des nodes
    allGrades = []
    for doc in tfidf:
        gradeDoc = 42 # à changer
        allGrades.append((gradeDoc,doc))

    # étape 4 : renvoyer les résultats (déjà écrit)
    out = []
    for (grade,url) in sorted(allGrades,reverse=True)[:10]:
        print("Selecting "+url+" with score "+str(grade))
        cursor.execute("SELECT title,content FROM webpages WHERE url=?",(url,))
        row=cursor.fetchone()
        if row:
            out.append((url,row[0],row[1]))
    return out
