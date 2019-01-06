'''
segment package

Read the image and extract the XMP markup that describes regions containing people.

Write out new images named after the person in the region.
'''
import xml.etree.ElementTree as ET

import cv2
import numpy


def findElements(root, pattern):
	'''Search the XML at root finding tags containing the pattern.'''
	l = []
	for e in root.iter():
		if pattern in e.tag:
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


	def encodeUserName(self):
		return self.name.replace(' ', '_')


	def decodeUserName(self):
		return self.name.replace('_', ' ')


	def extractImage(self, filename):
		original_image = cv2.imread(filename)
		(h, w, d) = original_image.shape
		x0 = int(self.x0*w)
		y0 = int(self.y0*h)
		x1 = int(self.x1*w)
		y1 = int(self.y1*h)
		return original_image[y0:y1, x0:x1]


	def writeSegment(self, filename):
		new_img = self.extractImage(filename)
		newFileName = self.encodeUserName()+ '.jpg'
		cv2.imwrite(newFileName, new_img)
		return newFileName


	def extractFace(self, filename):
		'''Save a greyscale version of the segment to include only the face.

		Based on tutorial in https://linuxhint.com/opencv-face-recognition/
		'''

		face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		image = self.extractImage(filename)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = face_detector.detectMultiScale(gray, 1.3, 5)

		count = 0
		for (x,y,w,h) in faces:
			cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 2)
			count += 1
			cv2.imwrite("User." + self.encodeUserName() + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])


def createSegments(filename):
	'''Read XMP data from the filename and create segments for each subject.'''

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