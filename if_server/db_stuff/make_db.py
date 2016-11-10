import sqlite3


#
#Scheme
#
scheme = """

CREATE TABLE address(
    host CHAR(255),
    temp Date,
    iface Int,
    ipv4 Char(20),
    mask Char(20),
    gate Char(20)
    );
"""

#
#Set up DB
#
conn = sqlite3.connect('example.db')
curse = conn.cursor()
curse.execute(scheme)
conn.commit()
conn.close()
