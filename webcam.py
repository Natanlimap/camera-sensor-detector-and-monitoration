# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import datetime
import sendEmail
hasToRecord = False 
isRecording = False
def setHasRecordTrue():
	global hasToRecord
	hasToRecord = True

def setHasRecordFalse():
	global hasToRecord
	hasToRecord = False



def setArguments():
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", help="path to the video file")
	ap.add_argument("-a", "--min-area", type=int, default=10000, help="minimum area size")
	return vars(ap.parse_args())

def setWebcam(args):
	if args.get("video", None) is None:
		vs = VideoStream(src=0).start()
		time.sleep(2.0)
	else:
		vs = cv2.VideoCapture(args["video"])
	return vs
def setInitialFrame(vs, args):
	frame = vs.read()
	return frame if args.get("video", None) is None else frame[1]

def drawImage(frame, frameDelta, text, thresh):
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), 
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)

def saveFrame(frame):
	cv2.imwrite("frame.jpg", frame)

def deleteImage():
	if(os.path.exists("frame.jpg")):
		os.remove("frame.jpg")

def main():
	global hasToRecord
	args = setArguments()
	vs = setWebcam(args)
	firstFrame = None
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output.avi', fourcc, 60.0, (640,  480))

	counter = 0
	while True:
		text = "Unoccupieqd"
		frame = vs.read()
		out.write(frame)		
	
		frame = imutils.resize(frame, width=500)

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		if firstFrame is None:
			firstFrame = gray
			continue

		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		

		thresh = cv2.dilate(thresh, None, iterations=5)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)


		for c in cnts:
			if cv2.contourArea(c) < args["min_area"]:
				deleteImage()
				setHasRecordFalse()
				continue	
			saveFrame(frame)		
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			text = "Occupied"
			
		

		drawImage(frame, frameDelta, text, thresh)
		sendEmail.send(1)



		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

	vs.stop() if args.get("video", None) is None else vs.release()
	cv2.destroyAllWindows()

main()