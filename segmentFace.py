'''
Read the image and extract the XMP markup that describes regions containing people.
Extract a greyscale image of each face and write to a file.
'''
from segments import segment, createSegments

filename = 'Family Picture.jpg'

segments = createSegments(filename)
for s in segments.values():
	s.extractFace(filename)
