import xml.etree.ElementTree as ET
tree = ET.parse('/Users/sanatmouli/Desktop/scraper/GenInfo_A0E60.xml')
root = tree.getroot()

var_tag = []
var_attrib = []
var_text = []

counter = 0

for child in root: 
	#print child.tag, child.attrib, child.text
	var_tag.append(child.tag)
	var_attrib.append(child.attrib)
	var_text.append(child.text)
	#counter = counter + 1

	if child.tag == '{urn:reuterscompanycontent:generalinformation03}IndustryClassification':

		for sub1child in child:
			#print sub1child.tag, sub1child.attrib, sub1child.text
			var_tag.append(sub1child.tag)
			var_attrib.append(sub1child.attrib)
			var_text.append(sub1child.text)

			if sub1child.tag == '{urn:reuterscompanycontent:generalinformation03}Taxonomy':
				for sub2child in sub1child:
					#print sub2child.tag, sub2child.attrib, sub2child.text
					var_tag.append(sub2child.tag)
					var_attrib.append(sub2child.attrib)
					var_text.append(sub2child.text)

	if child.tag == '{urn:reuterscompanycontent:generalinformation03}CompanyGeneralInfo':
		#print sub1child.tag, sub1child.attrib, sub1child.text
		var_tag.append(sub1child.tag)
		var_attrib.append(sub1child.attrib)
		var_text.append(sub1child.text)

	


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
