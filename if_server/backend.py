
import json
import web
import re
import datetime

validate_date = re.compile(r"^\d{4}-\d{2}-\d{2}$")
validate_ip = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
validate_num = re.compile(r"^\d+$")


#
#Web.py native ORM
#
db = web.database(dbn='sqlite',db='example.db')



#
#Create the insert query
#
#   The web.py ORM is less then ideal. 
#
def make_insert_query(host,today,iface,ipv4,mask,gate):
    if not validate_date.match(today):
        return (1, "Date malformed")
    if not validate_ip.match(ipv4):
        return (2, "IP address malformed")
    if not validate_ip.match(mask):
        return (3, "Subnet Mask malformed")
    if not validate_ip.match(gate):
        return (4, "Gateway malformed")
    if not validate_num.match(iface):
        return (5, "Interface malformed")
    return (0,r"INSERT INTO address VALUES ('%s','%s',%s,'%s','%s','%s');"%(host,today,iface,ipv4,mask,gate))




#
#Insert data into the DB
#
def insert_data(arg):
    date = str(datetime.date.today())
    item = json.loads(arg)
    host = item['host']
    i = 0
    for x in item['interfaces']:
        (err,msg) = make_insert_query(host,date,str(i),x[0],x[2],x[1])
        if err != 0:
            return (err,msg)
        db.query(msg)
    return (0,"Success!")


select_statement = """
SELECT * FROM address GROUP BY host ORDER BY temp
"""

#
#Get data
#
def get_data():
    return db.query(select_statement)
