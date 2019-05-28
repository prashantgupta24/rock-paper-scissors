import json
from os.path import abspath

import cv2

from vr import classifyImage

# Windows dependencies
# - Python 2.7.6: http://www.python.org/download/
# - OpenCV: http://opencv.org/
# - Numpy -- get numpy from here because the official builds don't support x64:
#   http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

# Mac Dependencies
# - brew install python
# - pip install numpy
# - brew tap homebrew/science
# - brew install opencv
# worked -
# pip install opencv-python


def captureImage():
    cap = cv2.VideoCapture(0)
    rock = img = cv2.imread('resources/rock.jpg', 0)
    paper = cv2.imread('resources/paper.jpg', 0)
    scissors = cv2.imread('resources/scissors.jpg', 0)

    while(True):
        ret, frame = cap.read()
        # if ret == True:
        #     frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        cv2.imshow('input', rgb)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            out = cv2.imwrite('resources/capture.jpg', frame)
            classified_class = classifyCurrentImage()
            cv2.destroyWindow('input')
            print(classified_class)
            cv2.imshow('image', rock)
            cv2.waitKey()
            cv2.destroyWindow('image')
            # break

    cap.release()
    cv2.destroyAllWindows()


def classifyCurrentImage():
    image_file = abspath('resources/capture.jpg')
    classes = classifyImage(image_file=image_file, threshold='0.6')
    #print(json.dumps(classes, indent=2))
    return classes[0]["class"]


if __name__ == "__main__":
    captureImage()
