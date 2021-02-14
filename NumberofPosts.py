import gzip
import xml.etree.ElementTree as ET

fl=0

input = gzip.open("./english.stackexchange.com/Posts.xml.gz", 'r')
treepost = ET.parse(input)
rootpost = treepost.getroot()

#print(rootpost[0].attrib)
for elempost in rootpost:
    if (elempost.attrib['PostTypeId']=='1'):
        fl+=1;

print(fl)



