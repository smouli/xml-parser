import xml.etree.ElementTree as ET
import re
import psycopg2
import sys
import pprint
import glob   

#query = "INSERT INTO testtable (testcolumn) VALUES (9)"
#cursor.execute(query)
#conn.commit()
#cursor.execute('SELECT * FROM testtable')
#records = cursor.fetchall()
#pprint.pprint(records)
#conn_string = "host='localhost' dbname='postgres' user='sanatmouli' password='secret'"

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
        for child in root:
            child.tag = stripNS(child.tag)
            if child.tag == 'Employees':
                Employees = child.text
                #print (Employees)
            elif child.tag == 'TotalSharesOut':
                TotalSharesOut = child.text
                TotalFloat = child.attrib["TotalFloat"]
                #print (TotalSharesOut)
                #print (TotalFloat)
            elif child.tag == 'CommonShareholders':
                CommonShareholders = child.text
                #print (CommonShareholders)
            elif child.tag == 'IncorporatedIn':
                IncorporatedIn = child.text
                IncorporatedInCountry = child.attrib["Country"]
                IncorporatedInDate = ""
                if "Date" in child.attrib:
                    IncorporatedInDate = child.attrib["Date"]
                
                #print (IncorporatedIn)
                #print (IncorporatedInCountry)
                #print (IncorporatedInDate)
        return (Employees,TotalSharesOut,TotalFloat,CommonShareholders,IncorporatedIn,IncorporatedInCountry,IncorporatedInDate)
    
def parseTextInfo(root):
    for child in root:
        child.tag = stripNS(child.tag)
        if child.attrib["Type"] == "Business Summary":
            businessSummary = child.text
            #print(businessSummary)
           
        elif child.attrib["Type"] == "Equity Composition":
            equityComposition = child.text
            #print(equityComposition)
        
        elif child.attrib["Type"] == "Analyst Footnotes":
            analystFootnotes = child.text
            #print(analystFootnotes)
            
        elif child.attrib["Type"] == "Financial Summary":
            financialSummary = child.text
            #print(financialSummary)
            
        
    return businessSummary,equityComposition,analystFootnotes,financialSummary

def parseFile(filename):
    
    root = initXML(filename)
    #ns = {'geninfo': 'urn:reuterscompanycontent:generalinformation03'}   
    for child in root: 
        child.tag = stripNS(child.tag)
        #print (child.tag)
        if child.tag == 'RepNo':
            RepNo = child.text
            values = value + (RepNo ,)
            columns = columns + ("repno" ,)
            print (RepNo)
            
        elif child.tag == 'CompanyName':
            CompanyName = child.text
            CompanyType = child.attrib["Type"]
            #print (CompanyName)
            #print (CompanyType)
            #CompanyType = CompanyType.spilt(':')
        
        elif child.tag == 'CompanyGeneralInfo':
            Employees,TotalSharesOut,TotalFloat,CommonShareholders,IncorporatedIn,IncorporatedInCountry,IncorporatedInDate = parseCompanyGeneralInfo(child)
        
        elif child.tag == 'ContactInfo':
            #Store it as XML
            ContactInfo = "TBD"
           
        elif child.tag == 'WebLinksInfo':
            #Store it as XML
            WebLinksInfo = "TBD"
            
        elif child.tag == 'TextInfo':
             businessSummary,equityComposition,analystFootnotes,financialSummary = parseTextInfo(child)
        
        elif child.tag == 'Advisors':
            Advisors = "TBD"
            
    pl = (RepNo, CompanyName, CompanyType, Employees, TotalSharesOut, TotalFloat, CommonShareholders, IncorporatedIn, IncorporatedInCountry, IncorporatedInDate, businessSummary, equityComposition, analystFootnotes, financialSummary, )
    query = "INSERT INTO geninfo03 (repno, CompanyName, CompanyType, Employees, \
                                    TotalSharesOut, TotalFloat, CommonShareholders, IncorporatedIn, \
                                    IncorporatedInCountry, IncorporatedInDate, businessSummary, \
                                    equityComposition, analystFootnotes, financialSummary) \
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, pl)
    conn.commit()
        
def main():
    (conn, cursor) = initDB()
    path = '/Users/sanatmouli/Desktop/GenTemp/*.xml'   
    files=glob.glob(path)   
    for file in files:     
        print ("Parsing file:", file)
        parseFile(file)
    
if __name__ == "__main__":
	main()
