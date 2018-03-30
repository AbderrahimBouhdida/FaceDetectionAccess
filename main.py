# main.py
import cv2 as cv
import sys,os,time


size = 1
lbp_classifier = 'Data/lbpcascade_frontalface.xml'
users_dir = 'Users'
data = 'Data/model.xml'
t = 0
active = True 
(im_width, im_height) = (110, 90)

# Start and load the recognizer model
model = cv.face.LBPHFaceRecognizer_create()
model.read(data)
# Load the Local Binary Pattern classifier
lbp_cascade = cv.CascadeClassifier(lbp_classifier)
# Open camera
camera = cv.VideoCapture(0)


# Create a list of images and a list of corresponding names
names={}
id = 0
for (subdirs, dirs, files) in os.walk(users_dir):

    # Loop through each folder named after the subject in the photos
    for subdir in dirs:
        names[id] = subdir
        id+=1

while active:
    
    # Loop until the camera is working
    working = False
    while(not working):
        # Put the image from the camera into 'frame'
        (working, frame) = camera.read()
        if(not working):
            print("Probleme avec la camera")
            time.sleep(1)
            t=t+1
            if t == 3 :
                print("probleme survenu le programme doit quitter !")
                sys.exit(0)


    # Convert to grayscalel
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Resize to speed up detection (optinal, change size above)
    mini = cv.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

    # Detect faces and loop through each one
    faces = lbp_cascade.detectMultiScale(mini,1.1,3)
    for i in range(len(faces)):
        face_i = faces[i]

        # Coordinates of face after scaling back by `size`
        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv.resize(face, (im_width, im_height))

        # Try to recognize the face
        prediction, confidence = model.predict(face_resize)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
        if confidence < 100 :
            # Write the name of recognized face
            cv.putText(frame,
               '%s - %.0f' % (names[prediction],confidence),
               (x-10, y-10), cv.FONT_HERSHEY_PLAIN,1,(255, 0, 0))
            # Grant accesss 

        else :
            cv.putText(frame,
               '%s - %.0f' % ('unknown',confidence),
               (x-10, y-10), cv.FONT_HERSHEY_PLAIN,1,(255, 0, 0))
            pause = 1
    # Show the image and check for ESC being pressed
    cv.imshow('Detection', frame)
    key = cv.waitKey(10)
    if key == 27:
        break
camera.release()
cv.destroyAllWindows()
