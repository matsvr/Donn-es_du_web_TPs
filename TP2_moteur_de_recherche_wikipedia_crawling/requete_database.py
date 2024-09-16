import sqlite3

conn = sqlite3.connect('data.db')
# test = conn.execute(
#     "SELECT COUNT(*) FROM webpages")
# test = conn.execute(
#     "SELECT COUNT(*) FROM responses")
# test = conn.execute(
#     "SELECT COUNT(*) FROM webpages WHERE queryURL == respURL")
test = conn.execute(
    "SELECT url FROM wordfreq WHERE mot == 'soleil' ORDER BY freq DESC LIMIT 1")
print(test.fetchall())
