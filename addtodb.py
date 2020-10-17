""" 
Developed by : Adem Boussetha
Email : ademboussetha@gmail.com
"""
import cv2
import datetime
import os
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
# Read the input image
#img = cv2.imread('test.png')
cap = cv2.VideoCapture(0)
print ("you're gonna be added to db face recognition.")
name = input("enter your name please : ")
dirname='images/'+name
os.makedirs(dirname)
while True:
	_, img = cap.read()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)

	for (x, y , w ,h) in faces:
		cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0 , 0), 3)
		filename= f'{name}-'+str(datetime.datetime.now()).replace(" ","_")+'.png'
		print(filename)
		dirname= dirname+"/"
		print(dirname)
		isWritten =cv2.imwrite(os.path.join(dirname,filename),img[y:y+h,x:x+w])
		if isWritten: 
			print("image is successfully saved as file")
	# Display the output
	cv2.imshow('img', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()