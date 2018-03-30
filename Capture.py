#Capture.py
import cv2 as cv
import sys,os,time  
lbp_classifier_face = 'Data/lbpcascade_frontalface.xml'
users_dir = 'Users'

(im_width, im_height) = (110, 90)
size = 1

lbp_cascade_face = cv.CascadeClassifier(lbp_classifier_face)
camera = cv.VideoCapture(0)
try:
    user_name = input("Donne le nom \n")
except:
    print("Vous devez entrer un nom")
    sys.exit(0)
path = os.path.join(users_dir, user_name)
if not os.path.isdir(path):
    os.mkdir(path)


# Generate name for image file
pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
     if n[0]!='.' ]+[0])[-1] + 1

# Beginning message
print("\nLe programmes va capturer 20 images. \
Deplacez votre tete pour augmenter la precision pendant le fonctionnement.\n")

# The program loops until it has 20 images of the face.
count = 0
pause = 0
t = 0
count_max = 20
while count < count_max:

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


    # Get image size
    height, width, channels = frame.shape

    # Flip frame
    frame = cv.flip(frame, 1, 0)

    # Convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect faces
    faces = lbp_cascade_face.detectMultiScale(gray)

    # We only consider largest face
    faces = sorted(faces, key=lambda x: x[3])
    if faces:
        face_i = faces[0]
        (x, y, w, h) = [v * size for v in face_i]

        face = gray[y:y + h, x:x + w]
        face_resize = cv.resize(face, (im_width, im_height))
        # Draw rectangle and write name
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv.putText(frame, '%s - %d/20'%(user_name , count), (x - 10, y - 10), cv.FONT_HERSHEY_PLAIN,
            1,(0, 255, 0))

        # Remove false positives
        if(w * 6 < width or h * 6 < height):
            print("Non claire")
        else:
            # To create diversity, only save every fith detected image
            if(pause == 0):
                print("enregistrement de la capture "+str(count+1)+"/"+str(count_max))

                # Save image file
                cv.imwrite('%s/%s.png' % (path, pin), face_resize)
                pin += 1
                count += 1
                pause = 1

    if(pause > 0):
        pause = (pause + 1) % 3
    cv.imshow('capture', frame)
    key = cv.waitKey(10)
    if key == 27:
        break
camera.release()
cv.destroyAllWindows()

