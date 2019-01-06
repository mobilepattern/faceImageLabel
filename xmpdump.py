import xml.etree.ElementTree as ET

def findElements(root, patt):
	l = []
	for e in root.iter():
		if patt in e.tag:
			l.append(e)
	return l

f = 'Family Picture.jpg'
with open(f, encoding='latin-1') as fd:
	d= fd.read()
	xmp_start = d.find('<x:xmpmeta')
	xmp_end = d.find('</x:xmpmeta')
	xmp_str = d[xmp_start:xmp_end+12]

	root = ET.fromstring(xmp_str)

	regions = findElements(root, 'li')

	for r in regions:
		name = r.attrib['{http://ns.microsoft.com/photo/1.2/t/Region#}PersonDisplayName']
		region = r.attrib['{http://ns.microsoft.com/photo/1.2/t/Region#}Rectangle']
		print(name, region)
