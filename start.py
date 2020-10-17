""" 
Developed by : Adem Boussetha
Email : ademboussetha@gmail.com
"""

import cv2
import requests
import faces
import os 
import datetime
import deep_learning_object_detection as objectdetection
import color_classification_image
#IN CASE YOU USE IP CAMERA
"""os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"
 IP CAMERA DATA
MOUVEMENT_CAMERA_IP="http://192.168.1.107:5000/"
CAPTURE_CAMERA_IP="rtsp://192.168.1.107:554/onvif2" 

def centrelazied ():
	if (faces.faceX != faces.xframe):
		move_dist=faces.faceX-faces.xframe
		print(move_dist)
		print(int((move_dist*11)/3))
		for i in range(int((move_dist*11)/3)):
			if (move_dist<0):
				movecamera.moveCamera(-1,0,MOUVEMENT_CAMERA_IP)
			else : 
				movecamera.moveCamera(1,0,MOUVEMENT_CAMERA_IP)
				print ("adam")
	if (faces.faceY != faces.yframe):
		move_dist=faces.faceY-faces.yframe
		for i in range(int((move_dist*11)/3)):
			if (move_dist<0):
				movecamera.moveCamera(0,-1,MOUVEMENT_CAMERA_IP)
			else : 
				movecamera.moveCamera(0,1,MOUVEMENT_CAMERA_IP)	"""
cap = cv2.VideoCapture(2)
current_time= datetime.datetime.now()
while True :
	ret, frame = cap.read()
	faces.facedetection(frame)
	cv2.imshow('frame',frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
