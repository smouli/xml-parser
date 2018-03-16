import xml.etree.ElementTree as ET
import re
import psycopg2
import sys
import pprint
import glob   # -*- coding: utf-8 -*-

def initDB():
	conn_string = "host='localhost' dbname='postgres' user='sanatmouli'"
	#print ("Connecting to database\n ->%s" % (conn_string))
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	print ("Connected!")
	return conn, cursor

def initXML(file):  
	tree = ET.parse(file)
	root = tree.getroot()
	return root

def stripNS(tag):
	return re.sub('{[^}]+}', '', tag, count=1)
    

def insertIntoDB(tablename, keyval, conn, cursor):
    
    columns = ','.join( k for k in keyval)
    placeholder = ','.join( "%s" for k in keyval)
    query = "INSERT INTO " + tablename + " (" + columns + ") VALUES (" + placeholder + ")"
    
    valTuple = ()
    for (k,v) in keyval.items():
        valTuple = valTuple + (v, )
        
    cursor.execute(query, valTuple)
    
def parseCoIDs(root):
    keyval = {}
    for child in root:
        #print (child.attrib)
        if child.attrib["Type"] == "RepNo":
            keyval["repno"] = child.text
        
        if child.attrib["Type"] == "CompanyName":
            keyval["CompanyName"] = child.text
            
        if child.attrib["Type"] == "IRSNo":
            keyval["IRSNo"] = child.text
            
        if child.attrib["Type"] == "CIKNo":
            keyval["CIKNo"] = child.text
            
    return keyval

def parseIssues(root):
    keyval = {}
    count = 0
    for child in root:
        #print (child.attrib)
        if count == 1:
            keyval["IssueName"] = child.text
        elif count == 2:
            keyval["Ticker"] = child.text
        elif count == 3:
            keyval["CUSIP"] = child.text
        elif count == 4:
            keyval["ISIN"] = child.text
        elif count == 5:
            keyval["RIC"] = child.text
        elif count == 6:
            keyval["SEDOL"] = child.text
        elif count == 7:
            keyval["DisplayRIC"] = child.text
        elif count == 8:
            keyval["InstrumentPI"] = child.text
        elif count == 9:
            keyval["QuotePI"] = child.text
        
        count = count + 1
    return keyval
    
def parseIssue(root):
    keyval = {}
    for child in root:
       # print (child.attrib)
       keyval["IssueID"] = child.attrib["ID"]
       keyval["IssueType"] = child.attrib["Type"]
       keyval["IssueDesc"] = child.attrib["Desc"]
       keyval["IssueOrder"] = child.attrib["Order"]
       retkeyval = parseIssues(child)
       temp = keyval.copy()
       temp.update(retkeyval)
       keyval = temp
    #print (keyval)
    return keyval
    
def parseCoGeneralInfo(root):
    keyval = {}
    for child in root:
        if child.tag == 'CoStatus':
            keyval["CoStatus"] = child.text
            keyval["CoStatusCode"] = child.attrib["Code"]
            
        if child.tag == 'CoType':
            keyval["CoType"] = child.text
            keyval["CoTypeCode"] = child.attrib["Code"]
            
        if child.tag == 'LastModified':
            keyval["LastModified"] = child.text
            
        if child.tag == 'LatestAvailableAnnual':
            keyval["LatestAvailableAnnual"] = child.text
        
        if child.tag == 'LatestAvailableInterim':
            keyval["LatestAvailableInterim"] = child.text
            
        if child.tag == 'ReportingCurrency':
            keyval["ReportingCurrency"] = child.text
            keyval["ReportingCurrencyCode"] = child.attrib["Code"]
            
        if child.tag == 'MostRecentExchange':
            keyval["MostRecentExchange"] = child.text
            keyval["MostRecentExchangeDate"] = child.attrib["Date"]
            
    return keyval
            
def parseIndustryInfo(root):
    keyval = {}
    count = 1
    for child in root:
        #print (child.attrib)
        if count == 1:
            keyval["Industry"] = child.text
            keyval["IndustryType"] = child.attrib["Type"]
            keyval["IndustryCode"] = child.attrib["Code"]
            keyval["IndustryMnem"] = child.attrib["Mnem"]
        
        if count == 2:
            keyval["Sector"] = child.text
            keyval["SectorType"] = child.attrib["Type"]
            keyval["SectorCode"] = child.attrib["Code"]
            keyval["SectorMnem"] = child.attrib["Mnem"]
            
        count = count + 1
         
    return keyval

def parseFile(filename, conn, cursor):
    
    root = initXML(filename)
    
    keyval = {}

    for child in root:
        child.tag = stripNS(child.tag)
        #print(child.tag)
        if child.tag == 'CoIDs':
            #print (child.attrib)
            retkeyval = parseCoIDs(child)
            temp = keyval.copy()
            temp.update(retkeyval)
            keyval = temp
        
        if child.tag == 'Issues':
            retkeyval = parseIssue(child)
            temp = keyval.copy()
            temp.update(retkeyval)
            keyval = temp
            
            
        if child.tag == 'CoGeneralInfo':
            retkeyval = parseCoGeneralInfo(child)
            temp = keyval.copy()
            temp.update(retkeyval)
            keyval = temp
        
        if child.tag == 'IndustryInfo':
            retkeyval = parseIndustryInfo(child)
            temp = keyval.copy()
            temp.update(retkeyval)
            keyval = temp
            
        if child.tag == 'Text':
            keyval["TextInfo"] = child.text
    #print (keyval)
        
    insertIntoDB("longbusiness", keyval, conn, cursor)
    conn.commit()

def main():
    (conn, cursor) = initDB()
    path = '/Users/sanatmouli/Desktop/LongBusiness/*.xml'   
    files=glob.glob(path)   
    for file in files:     
        print ("Parsing file:", file)
        parseFile(file, conn, cursor)
    
if __name__ == "__main__":
	main()