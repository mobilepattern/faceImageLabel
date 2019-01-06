import PIL.Image
img = PIL.Image.open('Family Picture.jpg')
exif_data = img._getexif()

import PIL.ExifTags
exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}

for k in exif:
	print(k)