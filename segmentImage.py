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
	'''Describes subsections of an image.

	Origin is in the upper left.
	'''

	def __init__(self, name, x0, y0, x1, y1):
		self.name = name
		self.x0 = x0
		self.x1 = x1

		self.y0 = y0
		self.y1 = y1


	def __str__(self):
		return "%s: x0=%s, y0=%s, x1=%s, y1=%s" % (self.name, self.x0, self.y0, self.x1, self.y1)

	def writeSegment(self, original_file):
		(h, w, d) = original_image.shape
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
			(x0, y0, xh, yh) = map(float, r.attrib['{http://ns.microsoft.com/photo/1.2/t/Region#}Rectangle'].split(','))
			segments[name] = segment(name, x0, y0, x0 + xh, y0 + yh)
	return segments

filename = 'Family Picture.jpg'
original_image = cv2.imread(filename)

segments = createSegments(filename)
for s in segments.values():
	s.writeSegment(original_image)

# Test the segmentation write code

# upperLeft = segment('upperLeft', 0.0, 0.0, 0.5, 0.5)
# upperRight = segment('upperRight', 0.5, 0.0, 1.0, 0.5)
# lowerLeft = segment('lowerLeft', 0.0, 0.5, 0.5, 1.0)
# lowerRight = segment('lowerRight', 0.5, 0.5, 1.0, 1.0)

# upperLeft.writeSegment(original_image)
# upperRight.writeSegment(original_image)
# lowerLeft.writeSegment(original_image)
# lowerRight.writeSegment(original_image)