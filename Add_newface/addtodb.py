import cv2
import datetime
import os
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
cap = cv2.VideoCapture(0)
print ("you're gonna be added to db face recognition.")
name = input("enter your name please : ")
dirname='images/'+name
if not os.path.exists(dirname):
	os.makedirs(dirname)
else : 
	print(f"a folder with name {name} already exists.")
path =dirname+'/'
while True:
	_, img = cap.read()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 4)

	for (x, y , w ,h) in faces:
		cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0 , 0), 3)
		filename= f'{name}-'+str(datetime.datetime.now()).replace(" ","_")+'.png'
		print(filename)
		# print(path)
		isWritten =cv2.imwrite(os.path.join(path,filename),img)
		if isWritten: 
			print("image is successfully saved as file")
	# Display the output
	cv2.imshow('img', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()