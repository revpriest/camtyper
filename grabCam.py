import numpy as np
import cv2

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)

radius = 5
keydown = True
labelMap = [
  ('_', '5', '3', '(', ' ', '(', '1', '9', '7'),
  ('v', 'f', 'w', 'k', ' ', 'q', 'm', 'p', 'b'),
  ('l', 's', 'n', 'c', ' ', 'h', 't', 'r', 'd'),
  ('alt', 'meta', 'altR', 'shift', ' ', 'shiftR', 'ctrl', 'metaR', 'ctrlR'),
  (' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '),
  (':', 'bs', 'x', 'g', ' ', 'z', 'j', '$', '!'),
  ('del', 'i', 'e', 'ret', ' ', 'o', 'a', 'u', 'y'),
  ('/', 'up', '-', 'left', ' ', 'right', '+', 'down', '*'),
  ('.', '6', '4', ',', ' ', '8', '2', '0', 'enter')
]
charMap = [
  (ord(' '), ord('5'), ord('3'), ord('('), ord(' '), ord('('), ord('1'), ord('9'), ord('7')),
  (ord('v'), ord('f'), ord('w'), ord('k'), ord(' '), ord('q'), ord('m'), ord('p'), ord('b')),
  (ord('l'), ord('s'), ord('n'), ord('c'), ord(' '), ord('h'), ord('t'), ord('r'), ord('d')),
  (18, 91, 225, 16, ord(' '), 16, 17, 93, 17),
  (ord(' '), ord(' '), ord(' '), ord(' '), ord(' '), ord(' '), ord(' '), ord(' '), ord(' ')),
  (ord(':'), 8, ord('x'), ord('g'), ord(' '), ord('z'), ord('j'), ord('$'), ord('!')),
  (46, ord('i'), ord('e'), 13, ord(' '), ord('o'), ord('a'), ord('u'), ord('y')),
  (ord('/'), 38, ord('-'), 37, ord(' '), 39, ord('+'), 40, ord('*')),
  (ord('.'), ord('6'), ord('4'), ord(','), ord(' '), ord('8'), ord('2'), ord('0'), 13)
]


modeMap = ['odd', 'c2', 'c1', 'meta', ' ', '!', 'vow', 'curs', 'even']

def getMax(img):
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(img)
	return maxLoc

def drawGrid(img, offset):
	cv2.line(img, (53+offset, 0), (53+offset, 240), (255,255,255), 2)
	cv2.line(img, (107+offset, 0), (107+offset, 240), (255,255,255), 2)
	
	cv2.line(img, (0+offset, 80), (160+offset, 80), (255,255,255), 2)
	cv2.line(img, (0+offset, 160), (160+offset, 160), (255,255,255), 2)

def drawLabels(img, offset, labelSet):
	font = cv2.FONT_HERSHEY_PLAIN
	colour = (255,255,255)
	scale = 1
	thickness = 2
	cv2.putText(img, labelSet[0], (offset+0, 40),  font, scale, colour, thickness)
	cv2.putText(img, labelSet[1], (offset+55, 40),  font, scale, colour, thickness)
	cv2.putText(img, labelSet[2], (offset+108, 40),  font, scale, colour, thickness)
	cv2.putText(img, labelSet[3], (offset+0, 120),  font, scale, colour, thickness)
	cv2.putText(img, labelSet[4], (offset+55, 120),  font, scale, colour, thickness)
	cv2.putText(img, labelSet[5], (offset+108, 120),  font, scale, colour, thickness)
	cv2.putText(img, labelSet[6], (offset+0, 200),  font, scale, colour, thickness)
	cv2.putText(img, labelSet[7], (offset+55, 200),  font, scale, colour, thickness)
	cv2.putText(img, labelSet[8], (offset+108, 200),  font, scale, colour, thickness)

def getRegion(point):
	if (point[0] < 60):
		region = 0
	elif (point[0] < 120):
		region = 1
	else:
		region = 2

	if (point[1] < 80):
		region += 0
	elif (point[1] < 160):
		region += 3
	else:
		region += 6

	return region

def outputChar(mode,key):
	print(chr(charMap[mode][key]))
	sys.stdout.write(chr(charMap[mode][key]))


cap = cv2.VideoCapture(0)
cap.set(3,320); #x
cap.set(4,240); #y
cap.set(5,1000); #FPS ???


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    flip = cv2.flip(frame,1)

    # Display the resulting frame
    #cv2.imshow('frame',flip)

    # Convert to greyscale
    grey = cv2.cvtColor(flip, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (radius, radius), 0)

    leftHalf = blur[0:240, 0:160]
    rightHalf = blur[0:240, 161:320]

    leftMaxLoc = getMax(leftHalf)
    rightMaxLoc = getMax(rightHalf)
    adjRightMaxLoc = (rightMaxLoc[0]+160, rightMaxLoc[1])


    drawGrid(flip, 0)
    drawGrid(flip, 160)
    cv2.line(flip, (160, 0), (160, 240), (255, 0, 0), 2)
    drawLabels(flip, 0, modeMap)
    mode = getRegion(leftMaxLoc)
    drawLabels(flip, 160, labelMap[mode])
    key = getRegion(rightMaxLoc)
    if (key != 4):
    	if (not keydown):
    		outputChar(mode,key)
    		keydown = True
    else:
    	keydown = False

    cv2.circle(flip, leftMaxLoc, radius+6, (0, 0, 255), 2)
    cv2.circle(flip, adjRightMaxLoc, radius+6, (0, 255, 255), 2)

    cv2.imshow('frame',flip)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

