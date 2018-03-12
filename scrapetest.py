import xml.etree.ElementTree as ET
import re
import psycopg2
import sys
import pprint

#query = "INSERT INTO testtable (testcolumn) VALUES (9)"
#cursor.execute(query)
#conn.commit()
#cursor.execute('SELECT * FROM testtable')
#records = cursor.fetchall()
#pprint.pprint(records)
#conn_string = "host='localhost' dbname='postgres' user='sanatmouli' password='secret'"

def initDB():
	conn_string = "host='localhost' dbname='postgres' user='sanatmouli'"

	# print the connection string we will use to connect
	print "Connecting to database\n ->%s" % (conn_string)
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()

	print "Connected!\n"

	return conn, cursor


def initXML():
	tree = ET.parse('/Users/sanatmouli/Desktop/scraper/GenInfo_A0E60.xml')
	root = tree.getroot()
	return root

def stripNS(tag):
	return re.sub('{[^}]+}', '', tag, count=1)

def main():
	(conn, cursor) = initDB()
	root = initXML()

	#ns = {'geninfo': 'urn:reuterscompanycontent:generalinformation03'}

	for child in root: 
		child.tag = stripNS(child.tag)
		if child.tag == 'ContactInfo':
			print (child.tag,child.text,child.attrib)
			



if __name__ == "__main__":
	main()
