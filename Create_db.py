# coding= utf-8
import  sqlite3

db = sqlite3.connect('test.db')

cur = db.cursor()

com1 = 'create table memory (id integer, host string, mem_free integer, mem_usage integer, mem_toeal integer, time integer)'
cur.execute(com1)