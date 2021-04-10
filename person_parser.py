import os
import lxml.etree as ET

myFile = "input/person/"
myOutput = "output/person/"
myXslt = "xslt/Person.xsl"

def parser_person():
    for root, dirs, files in os.walk(myFile):
        for item in files:
            if item.endswith(('.xml')):
                dom = ET.parse( root + "/" + item)
                xslt = ET.parse(myXslt)
                transform = ET.XSLT(xslt)
                newdom = transform(dom)
                infile = (ET.tostring(newdom, pretty_print=True, encoding='utf-8'))
                outfile = open(myOutput + item, 'wb')
                outfile.write(infile)