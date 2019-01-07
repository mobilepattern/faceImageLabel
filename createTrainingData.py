'''
Create training data.

python createTrainingData.py <dir>

This goes recursively through the directory, finding all image files and creates a set of training
images in .training
# TODO - make this work in the source directory by default.

The images are of the form
User.<name>.index.jpg
where
<name> is the name of the user with " " replaced with _

Based on 
https://linuxhint.com/opencv-face-recognition/
'''

import sys
from os import path, walk

from segments import segment, createSegments


def isImageFile(f):
	return f.endswith('jpg')


def processImage(imageFileName, targetDirectory, count=0):
	segments = createSegments(imageFileName)
	for s in segments.values():
		s.extractFace(imageFileName, directory=targetDirectory, count=count)


def walkRoot(root, trainingDir):
	count = 0
	for r, dirs, files in walk(root):
		if trainingDir in dirs:
			dirs.remove(trainingDir)
		for f in files:
			if isImageFile(f):
				count = count + 1
				processImage(path.join(r, f), trainingDir, count=count)


if __name__ == '__main__':
	root = sys.argv[1]

	# Check to see the .training directory exists


	# Do the work
	walkRoot(root, '.training')
