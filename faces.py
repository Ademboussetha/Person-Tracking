""" 
Developed by : Adem Boussetha
Email : ademboussetha@gmail.com
"""

import numpy as np
import cv2
import pickle
import os
import time
import serial
import json
import deep_learning_object_detection as objectdetection
import color_classification_image
import datetime
import notification
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"
# face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")
labels={}
xframe=0
yframe=0
faceX=0
faceY=0
ser = serial.Serial(
		'/dev/ttyACM0', #this is the port for ubuntu users, if u're in windows it should be something like COM5 
		baudrate=9600, 
		timeout=1)
with open("labels.pickle","rb") as f:
	og_labels=pickle.load(f)
	labels={v:k for k,v in og_labels.items()}
PERSON=""
def facedetection(frame):
	previous = time.time()
	gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	(n, p) = frame.shape[:2]
	global xframe
	global yframe
	xframe= int(p/2)
	yframe= int (n/2)
	# print(xframe,yframe)
	#this instruction is just for checking 
	# cv2.circle(frame,(320,0),6,(0,255,0),thickness=6)
	current_time=datetime.datetime.now()
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
	#Dans le cas ou il n ya pas de visage du tt dans le frame
	if len(faces)==0:
		print("no faces found")
		cv2.imwrite("noface.png",frame)
		with open ('data.json') as f :
			data = json.load(f)
		print(data['persons'][0]['shirt'])
		objectdetection.objecttracking("noface.png")
		if objectdetection.who=="person":
			bodyColor=color_classification_image.getColor("outputobjectdetection.png")
			with open ('data.json') as f :
				data = json.load(f)
			if bodyColor==data['persons'][0]['shirt'] :
				xcenter= int((objectdetection.startX+ objectdetection.endX)/3)
				ycenter= int((objectdetection.startY+ objectdetection.endY)/3)
				cv2.circle(frame,(xcenter,ycenter),6,(0,255,0),thickness=6)
				moving(xcenter,ycenter)
		else : 
			minute = (datetime.datetime.now()-current_time ).total_seconds()/60
			rounded_minute = round(minute)
			hours=(rounded_minute/60)
			print("unknown")
			#we send just one notification/day so we wont spam the email.
			if hours>22.0: 
				now = datetime.datetime.now()
				current_time = now.strftime("%H:%M:%S")
				notification.send_mail(current_time)			
	for (x, y, w, h) in faces:
		roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
		current = time.time()
		delta += current - previous
		previous = current
		#recognize?
		id_,conf=recognizer.predict(roi_gray)
		global idk
		if conf >=45 and conf<=85:
			name=labels[id_]
			cv2.imwrite("knownobjectdetection.png",frame)
			objectdetection.objecttracking("knownobjectdetection.png")
			idk=color_classification_image.getColor("outputobjectdetection.png")
			jsondata={}
			jsondata['persons']=[]
			jsondata['persons'].append({
				"name": name,
				"shirt": idk,
			})
			with open("data.json",'w') as f :
				json.dump(jsondata,f)
			font =cv2.FONT_HERSHEY_SIMPLEX
			color =(255,255,255)
			stroke =2
			cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
			print (f"Person found : {name.capitalize()}")
			match = True
		else :
			match = False
			print ("Person found : Unknown person")
			font =cv2.FONT_HERSHEY_SIMPLEX
			color =(255,255,255)
			stroke =2
			cv2.imwrite("unknownobjectdetection.png",frame)
			objectdetection.objecttracking("unknownobjectdetection.png")
			idk=color_classification_image.getColor("outputobjectdetection.png")
			cv2.putText(frame,"unknown",(x,y),font,1,color,stroke,cv2.LINE_AA)
		
		cv2.circle(frame,(xframe,yframe),6,(0,255,0),thickness=6)
		color = (255, 0, 0) #BGR 0-255 
		stroke = 2
		end_cord_x = x + w
		end_cord_y = y + h
		cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
		global faceX
		global faceY
		faceX = int(x + (w / 2.0))
		faceY = int(y + (h / 2.0))
		cv2.circle(frame,(faceX,faceY),6,color,thickness=6)
		if  (match is True):
			moving(faceX,faceY)
		else : 
			with open('data.json') as f :
				data=json.load(f)
			#In case we found a face but we dont recognize it 
			if data['persons'][0]['shirt']== idk :
				xcenter= int((objectdetection.startX+ objectdetection.endX)/2)
				ycenter= int((objectdetection.startY+ objectdetection.endY)/3)
				moving(xcenter,ycenter)
			else : 
				minute = (datetime.datetime.now()-current_time ).total_seconds()/60
				rounded_minute = round(minute)
				hours=(rounded_minute/60)
				print ("hours : ",hours)
				print("unknown")
				#we send just one notification/day so we wont spam the email.
				if hours>22.0: 
					now = datetime.datetime.now()
					current_time = now.strftime("%H:%M:%S")
					notification.send_mail(current_time)		
				
def moving(faceX,faceY):
	if faceX > 350:                  #The following code blocks check if the face is    
		ser.write('L'.encode()) #on the left, right, top or bottom with respect to the 
		time.sleep(0.01)        #center of the frame. 
	elif faceX < 290:                #If any of the conditions are true, it send a command to
		ser.write('R'.encode()) #the arduino through the serial bus.
		time.sleep(0.01)
	else:
		ser.write('S'.encode())
		time.sleep(0.01)

	if faceY > 210:
		ser.write('D'.encode())
		time.sleep(0.01)
	elif faceY < 270:
		ser.write('U'.encode())
		time.sleep(0.01)
	else:
		ser.write('S'.encode())
		time.sleep(0.01)