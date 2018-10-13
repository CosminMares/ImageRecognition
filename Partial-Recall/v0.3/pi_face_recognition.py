from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
from threading import Timer
import argparse
import imutils
import pickle
import time
import cv2
import timeit
import os

CLASSIFIER_FILE = 'haarcascade_frontalface_default.xml'
PICKLE_FILE = 'encodings.pickle'
CONFIG_NAMES_FILE = 'names.config'

activeNames = {}
timeout = 7
isPi = True
debugMode = False

data = pickle.loads(open(PICKLE_FILE, "rb").read())
detector = cv2.CascadeClassifier(CLASSIFIER_FILE)

def getConfigInfo(activeNames):
	f = open(CONFIG_NAMES_FILE,'r')
	for line in f:
		if not line.startswith('#'):
			activeNames.update({line.strip():True})
	f.close()

def switchNameActiveState():
	for name in activeNames:
		activeNames[name] = True

getConfigInfo(activeNames)

# initialize the video stream and allow the camera sensor to warm up
if isPi:
	vs = VideoStream(usePiCamera=True).start()
else:
	vs = VideoStream(src=0).start()

time.sleep(2.0)

# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream and resize it
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	
	# convert the input frame from (1) BGR to grayscale (for face
	# detection) and (2) from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #to try only with 

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(rgb, scaleFactor=1.1, #this was changed to rgb from gray
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
	
	# OpenCV returns bounding box coordinates in (x, y, w, h) order
	# but we need them in (top, right, bottom, left) order, so we
	# need to do a bit of reordering
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []
	name = "Unknown"
	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		
		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1
				
			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
		
		# update the list of names
		names.append(name)

	if (debugMode):	
		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# draw the predicted face name on the image
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 0), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				0.75, (0, 255, 0), 2)

	# decide and playback the name
	if(name != "Unknown" and activeNames.get(name)):
		speechFilename=name + ".mp3"
		os.system("mpg321 -q " + "./audio/" + speechFilename)
		activeNames.update({name:False})
		t = Timer(timeout,switchNameActiveState)
		if (not t.is_alive()):
			t.start()

	# display the image to our screen
	if debugMode:
		cv2.imshow("Frame", frame)
	
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
