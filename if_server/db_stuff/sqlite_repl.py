
#
#This is a quick script for debugging the state of sqlite3
#

import sqlite3
import sys

print "Welcome to the simple SQLITE3 REPL"
print "On windows wrap arguments in single '' quotes"
print ""
print ":q       to quit"
print ":c       to commit"
print ":r       to roll back"
print ":cq      to commit AND exit"
print ":rq      to roll back AND quit"
print ":h       to see this help text"
sys.stdout.flush()
#set up connection
conn = {}
connection_str = input("DB Path: ")
try:
    conn = sqlite3.connect(connection_str)
except:
    print "Could not connect to %s"%connection_str
    print "Error %s"%str(sys.exc_info()[0])
    sys.exit(1)

cursor = conn.cursor()

while True:
    query = input("Query: ")
    if query == ":cq":
        conn.commit()
        conn.close()
        sys.exit(0)
    if query == ":q":
        sys.exit(0)
    if query == ":c":
        conn.commit()
        continue
    if query == ":r":
        conn.rollback()
        continue
    if query == ":help" or query == ":h":
        print ":q       to quit"
        print ":c       to commit"
        print ":r       to roll back"
        print ":cq      to commit AND exit"
        print ":rq      to roll back AND quit"
        print ":h       to see this help text"
        sys.stdout.flush()
        continue
    out = {}
    try:
        print "Running..."
        for row in cursor.execute(query):
            print str(row)
    except:
        print "ERROR!!!\nERROR!!!"
        print "Query: %s"%query
        print "%s"%str(sys.exc_info()[0])
        print "ERROR!!!\nERROR!!!"
    sys.stdout.flush()


