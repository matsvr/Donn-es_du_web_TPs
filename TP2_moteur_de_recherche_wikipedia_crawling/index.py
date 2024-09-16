#!/usr/bin/env python3

import sqlite3
import re
from math import log
from shared import extractListOfWords, stem
from collections import defaultdict
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
conn.execute("DROP TABLE IF EXISTS wordfreq")
# On créer des dictionnaires pour stocker les résultats avant de les mettre dans la base de données

# associe à une paire (mot-clef,URL) un compte du nombre d'occurrence
invertedIndex = defaultdict(int)
# associe à un mot-clef une liste d'URL avec ce mot-clef
docWithKW = defaultdict(set)
lenDoc = defaultdict(int)  # associe à chaque URL son nombre de mots
nbDocs = 0  # nombre total de documents


def countFreq(L):
    freq_dct = {}
    for w in L:
        w = stem(w)
        if w in freq_dct:
            freq_dct[w] += 1
        else:
            freq_dct[w] = 1
    return freq_dct.items()


cursor.execute("SELECT content,URL FROM webpages")
while True:
    row = cursor.fetchone()
    if not row:
        break
    # un tour de boucle par page
    # compléter ici
    # 1 - Calcul de l'index inversé
    #     utiliser extractListOfWords pour récupérer les mots à partir du contenu des pages
    wordlist = extractListOfWords(row[0])
    freq_count = countFreq(wordlist)
    for word, freq in freq_count:
        invertedIndex[(word, row[1])] = freq

    # 2- Calcul de l'IDF
    nbDocs = len(cursor.fetchall())
    for elt in row[1]:
        if elt in invertedIndex.keys():
            lenDoc[elt] += 1
        else:
            lenDoc[elt] = 1

# Stockage dans la base de données des résultats
conn.execute("CREATE TABLE wordfreq (mot TEXT, url TEXT, freq INT)")
for a, b in (invertedIndex.items()):
    conn.execute(
        "INSERT INTO wordfreq (mot, url, freq) VALUES (?,?,?)", (a[0], a[1], b))

# Rajout des index sur les colonnes qui stockent les keywords
conn.execute("CREATE INDEX wordfreq_idx ON wordfreq (mot)")

# Laisser cette opération commit à la fin sinon SQLite3 ne sauve pas
# vos opérations
conn.commit()
