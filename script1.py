import xml.etree.ElementTree as ET
tree = ET.parse('/Users/sanatmouli/xml-parser/GenInfo_A0E60.xml')
root = tree.getroot()

var_tag = []
var_attrib = []
var_text = []

counter = 0

for child in root: 
	print (child.tag, child.text, child.attrib)
	counter = counter + 1

	if child.tag == '{urn:reuterscompanycontent:generalinformation03}IndustryClassification':
		# Taxonomy
		for sub1child in child:
			print (sub1child.tag, sub1child.attrib)
			# Detail
			if sub1child.tag == '{urn:reuterscompanycontent:generalinformation03}Taxonomy':
				for sub2child in sub1child:
					print (sub2child.tag, sub2child.attrib)

	if child.tag == '{urn:reuterscompanycontent:generalinformation03}CompanyGeneralInfo':
		# Employees
		for sub1child in child:
			print (sub1child.tag, sub1child.text, sub1child.attrib)

	if child.tag == '{urn:reuterscompanycontent:generalinformation03}IssueInformation':
		for sub1child in child:
			print (sub1child.tag, sub1child.attrib) # print issue
			# Issuedetails
			if sub1child.tag == '{urn:reuterscompanycontent:generalinformation03}IssueDetails':
				for sub2child in sub1child:
					print (sub2child.tag, sub2child.attrib, sub2child.text)





	#var_tag.append(child.tag)
	#var_attrib.append(child.attrib)
	#var_text.append(child.text)
	#print(child.tag, child.attrib, child.text)
	
print 'tags:'
for temp in var_tag:
	print temp

print 'attributes:'
for temp in var_attrib:
	print temp
	
print 'text:'
for temp in var_text:
	print temp