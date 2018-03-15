import xml.etree.ElementTree as ET
import re
import psycopg2
import sys
import pprint
import glob   

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


def parseCompanyGeneralInfo(root):
        keyval = {}
        for child in root:
            child.tag = stripNS(child.tag)
            if child.tag == 'Employees':
                keyval["Employees"] = child.text
                
            elif child.tag == 'TotalSharesOut':
                keyval["TotalSharesOut"] = child.text
                keyval["TotalFloat"] = child.attrib["TotalFloat"] # 2nd TotalFloat is from the XML
    
            elif child.tag == 'CommonShareholders':
                keyval["CommonShareholders"] = child.text
                #print (CommonShareholders)
            elif child.tag == 'IncorporatedIn':
                if "IncorporatedIn" in child.attrib:
                    keyval["IncorporatedIn"]= child.text
                if "Country" in child.attrib:
                    keyval["IncorporatedInCountry"] = child.attrib["Country"]
                if "Date" in child.attrib:
                    #
                    #In one file the date is of the form YYYY-MM. Postgres wants a YYYY-MM-DD. 
                    #Therefore, I am adding 01 to DD if such a string exists
                    #
                    dt = child.attrib["Date"]
                    if re.match('^....-..$', dt):
                        dt = dt + "-01"
                    keyval["IncorporatedInDate"] = dt
        
        return keyval

    
def parseTextInfo(root):
    keyval = {}
    for child in root:
        child.tag = stripNS(child.tag)
        if child.attrib["Type"] == "Business Summary":
            keyval["businessSummary"] = child.text
            #print(businessSummary)
           
        elif child.attrib["Type"] == "Equity Composition":
            keyval["equityComposition"] = child.text
            #print(equityComposition)
        
        elif child.attrib["Type"] == "Analyst Footnotes":
            keyval["analystFootnotes"] = child.text
            #print(analystFootnotes)
            
        elif child.attrib["Type"] == "Financial Summary":
            keyval["financialSummary"] = child.text
        
    return keyval

def parseTaxonomy(root):
    keyValList = []
    for child in root:
        child.tag = stripNS(child.tag)
        taxonomyType = child.attrib["Type"] 
        for subchild in child:
            keyval = {}
            keyval["taxonomyType"] = taxonomyType
            keyval["Code"] = subchild.attrib["Code"]
            keyval["Description"] = subchild.attrib["Description"]
            keyval["Orders"] = subchild.attrib["Order"]
            
        keyValList.append(keyval)
        
    return keyValList


def insertIntoDB(tablename, keyval, conn, cursor):
    
    columns = ','.join( k for k in keyval)
    placeholder = ','.join( "%s" for k in keyval)
    query = "INSERT INTO " + tablename + " (" + columns + ") VALUES (" + placeholder + ")"
    
    valTuple = ()
    for (k,v) in keyval.items():
        valTuple = valTuple + (v, )
        
    cursor.execute(query, valTuple)
    

def parseFile(filename, conn, cursor):
    
    root = initXML(filename)

    keyval = {}
    #ns = {'geninfo': 'urn:reuterscompanycontent:generalinformation03'}   
    for child in root: 
        child.tag = stripNS(child.tag)
        #print (child.tag)
        if child.tag == 'RepNo':        
            keyval["repno"] = child.text

            
        elif child.tag == 'CompanyName':
            keyval["CompanyName"] = child.text
            keyval["CompanyType"] = child.attrib["Type"]

        
        elif child.tag == 'IndustryClassification':
            taxkeyvalList = parseTaxonomy(child)
            
            
        elif child.tag == 'CompanyGeneralInfo':
            retkeyval = parseCompanyGeneralInfo(child)
            temp = keyval.copy()
            temp.update(retkeyval)
            keyval = temp
        
#        elif child.tag == 'ContactInfo':
#            keyval["ContactInfo"] = "TBD"
#           
#        elif child.tag == 'WebLinksInfo':
#            keyval["WebLinksInfo"] = "TBD"
            
        elif child.tag == 'TextInfo':
             retkeyval = parseTextInfo(child)
             temp = keyval.copy()
             temp.update(retkeyval)
             keyval = temp
        
#        elif child.tag == 'Advisors':
#            keyval["Advisors"] = "TBD"
            
    
    # 
    # Synthesize the values for geninfo03 from keyval. 
    # Create a Query and Execute
    #
    insertIntoDB("genInfo03", keyval, conn, cursor)
    
    
    #
    # taxkeyvalList is a list of hashes one for each row
    # Synthesize the query and execute
    #
    for taxRow in taxkeyvalList:
        #
        taxRow["repno"] = keyval["repno"]
        insertIntoDB("geninfo03_tax", taxRow, conn, cursor)
        
    conn.commit()
        
def main():
    (conn, cursor) = initDB()
    path = '/Users/sanatmouli/Desktop/GenInfo03/*.xml'   
    files=glob.iglob(path)   
    count = 1
    for file in files:     
        print ("Parsing file:", file, count)
        parseFile(file, conn, cursor)
        count = count + 1
    
if __name__ == "__main__":
	main()
