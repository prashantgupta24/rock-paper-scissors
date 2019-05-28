import json
from os.path import abspath

from image import captureImage
from vr import classifyImage

while True:
    captureImage()
    image_file = abspath('resources/capture.jpg')
    classes = classifyImage(image_file=image_file, threshold='0.6')
    print(json.dumps(classes, indent=2))
