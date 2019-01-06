import xml.etree.ElementTree as ET

import cv2
import numpy

def findElements(root, patt):
	l = []
	for e in root.iter():
		if patt in e.tag:
			l.append(e)
	return l


class segment:
	def __init__(self, name, x0, y0, xh, yh):
		self.name = name
		self.x0 = x0
		self.x1 = x0 + xh

		self.y0 = y0
		self.y1 = y0 + yh


	def __str__(self):
		return "%s: x0=%s, y0=%s, x1=%s, y1=%s" % (self.name, self.x0, self.y0, self.x1, self.y1)

	def writeSegment(self, original_image):
		x0 = int(self.x0*w)
		y0 = int(self.y0*h)
		x1 = int(self.x1*w)
		y1 = int(self.y1*h)
		print(self.name, x0, y0, x1, y1)
		new_img = original_image[y0:y1, x0:x1]
		(nw, nh, nd) = new_img.shape
		print(self.name, nw, nh, nd)
		cv2.imwrite(self.name.replace(' ', '') + '.jpg', new_img)

def createSegments(filename):
	segments = {}

	with open(filename, encoding='latin-1') as fd:
		d= fd.read()
		xmp_start = d.find('<x:xmpmeta')
		xmp_end = d.find('</x:xmpmeta')
		xmp_str = d[xmp_start:xmp_end+12]

		root = ET.fromstring(xmp_str)

		regions = findElements(root, 'li')

		for r in regions:
			name = r.attrib['{http://ns.microsoft.com/photo/1.2/t/Region#}PersonDisplayName']
			region = r.attrib['{http://ns.microsoft.com/photo/1.2/t/Region#}Rectangle'].split(',')
			segments[name] = segment(name, 
			                         float(region[0]), float(region[1]), float(region[2]), float(region[3]))
	return segments

filename = 'Family Picture.jpg'

segments = createSegments(filename)

img = cv2.imread(filename)
(w, h, d) = img.shape

print(w, h, d)

for s in segments.values():
	s.writeSegment(img)