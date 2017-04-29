from django.test import TestCase
import MySQLdb as mdb
db = mdb.connect('localhost', 'root', '', 'crowdfunding');
cur = db.cursor()
cur.execute("SELECT * FROM user")

r = cur.fetchall()
for row in r:
    print(row)
