import xml.etree.ElementTree as ET
import urllib.request
import ssl
from xml.dom import minidom
import configparser
import os
import json

config = configparser.ConfigParser()
config.read('wallboard.ini')

def makedir(dir):
	try:
		os.makedirs(dir)
	except OSError:
		pass

def recurse_tree(node,queue):
    for child in node.getchildren():
        if child.text == queue:
            yield node.attrib
        for subchild in recurse_tree(child,queue):
            yield subchild

ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
tree = ET.parse(urllib.request.urlopen('http://mcmillanworld.co.uk/xml/wbcalltype.xml', context=ctx), ET.XMLParser(encoding='utf-8'))
root = tree.getroot()
#dom = minidom.parse(urllib.request.urlopen(config['WBCallTypePermalinks']['ITSD']))



#for node in dom.getElementsByTagName('column'):  # visit every node <bar />
#	print(node.toxml())


#for row in root.iterfind('row[@index="0"]/column'):
def xmltotext():
    for row in root.iterfind('row[@index="0"]'):
        qname=row.find('column[@name="QName"]').text
        print(qname)
        for column in row.iterfind('column'):
            filename=(qname + '.' + column.get('name') + ".txt")
            print(column.text)
            file = open(filename,'w')  
            file.write(column.text)       
            file.close()

def xmltojson():
    file = open('wbcalltype.json','w')
    file.write('{\n')
    file.close()
    rcount = 1
    rcount2 = 1
    for row in root.iterfind('row'):
        rcount += 1
    for row in root.iterfind('row'):
        rcount2 += 1
        CTName=row.find('column[@name="CTName"]').text
        file = open('wbcalltype.json','a')
        file.write("\t\""+CTName+"\" : {\n")
        count = 1
        for column in row.iterfind('column'):
            file = open('wbcalltype.json','a') 
            if count == 1:
                count = 2
            else:
                file.write(",\n")
            file.write("\t\t\""+column.get('name')+"\" : \""+column.text+"\"")       
        if rcount2 == rcount:
            file.write("\t}\n")
        else:
            file.write("\t},\n")
    file.write("}")
    file.close()  

ctdict = {}

def xmltodict():
    # https://www.programiz.com/python-programming/nested-dictionary
    for row in root.iterfind('row'):
        CTName=row.find('column[@name="CTName"]').text
        ctdict[CTName] = {} 
        for column in row.iterfind('column'):
            name = column.get('name')
            ctdict[CTName][name] = column.text
        #for 

#        qd = row.get('name')
#        qn = report+'.'+str(row.get('name'))
#        qs = row.text
#        print (qn, qs)
xmltodict()

# CT Dictionary to JSON
with open('result.json', 'w') as fp:
    json.dump(ctdict, fp)


# Threashold test
print(ctdict['CT_ITSD_EXIS']['CIQ'], ctdict['CT_ITSD_EXIS']['CIQAmber'], ctdict['CT_ITSD_EXIS']['CIQRed'])
if ctdict['CT_ITSD_EXIS']['CIQ'] >= ctdict['CT_ITSD_EXIS']['CIQRed']:
    print('Red')
elif ctdict['CT_ITSD_EXIS']['CIQ'] >= ctdict['CT_ITSD_EXIS']['CIQAmber']:
    print('Amber')
elif ctdict['CT_ITSD_EXIS']['CIQ'] <= ctdict['CT_ITSD_EXIS']['CIQAmber']:
    print('Green')

print('Done')

