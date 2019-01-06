'''
Read the image and extract the XMP markup that describes regions containing people.

Write out new images named after the person in the region.
'''
from segments import segment, createSegments

filename = 'Family Picture.jpg'

segments = createSegments(filename)
for s in segments.values():
	newFileName = s.writeSegment(filename)
	print("Saving ", newFileName)
