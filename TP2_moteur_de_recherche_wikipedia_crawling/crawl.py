#!/usr/bin/env python3

import requests
import re
from shared import neighbors, title, getPage
import sqlite3
conn = sqlite3.connect('data.db')

conn.execute("DROP TABLE IF EXISTS webpages")  # delete the table if it exists
conn.execute("DROP TABLE IF EXISTS responses")
# create a table for webpages
conn.execute("CREATE TABLE webpages (title TEXT, content TEXT, URL TEXT)")
# create a table to store which queried url returned what url
conn.execute("CREATE TABLE responses (queryURL TEXT, respURL TEXT)")


# ---------------------------------------------------


# YOUR CODE GOES HERE

# you will need the following functions from shared (already imported):
# - neighbors(content) that takes a page content and returns the links it finds in the page content
# - title(content) returning the title of a page
# - getPage(queryURL) returning a pair (response URL, content) for a query URL
#
#
# You will also need to insert data in the database which you can do like this
#
#  conn.execute("INSERT INTO responses (queryURL, respURL) VALUES (?,?)",(a,b))
#
# to insert a tuple (a,b) where a is the queryURL and b is the respURL
#

url_a_crawler = "https://wiki.jachiet.com/wikipedia_fr_climate_change_mini/"

todo = [url_a_crawler]
webpages = set(todo)
while len(todo):
    page = todo.pop()
    print(page)
    page_content, page_url = getPage(page)
    webpages_title = title(page_content)
    conn.execute("INSERT INTO webpages (title, content, URL) VALUES (?,?,?)",
                 (webpages_title, page_content, page_url))
    conn.execute("INSERT INTO responses (queryURL, respURL) VALUES (?,?)",
                 (page, page_url))
    for nxt in neighbors(page_content, page_url):
        if nxt not in webpages:
            todo.append(nxt)
            webpages.add(nxt)


test = conn.execute("SELECT COUNT(*) FROM webpages LIMIT 10")
print(test.fetchall())

# ---------------------------------------------------

# for future application we create indexes (speeds up querying time )
conn.execute("CREATE INDEX webpages_idx ON webpages (URL)")
conn.execute("CREATE INDEX responses_idx ON responses (queryURL)")

conn.commit()
conn.close()
