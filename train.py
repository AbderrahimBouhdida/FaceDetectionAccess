#train.py
import cv2 as cv
import numpy as np
import sys,os

size = 1

users_dir = 'Users'
data = 'Data/model.xml'
print('Training...')
# Get the folders containing the training data
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(users_dir):

    # Loop through each folder named after the subject in the photos
    for subdir in dirs:
        names[id] = subdir
        user = os.path.join(users_dir, subdir)
        # Loop through each photo in the folder
        for filename in os.listdir(user):

            # Skip non-image formates
            f_name, f_extension = os.path.splitext(filename)
            if(f_extension.lower() not in
                    ['.png','.jpg','.jpeg','.gif','.pgm']):
                print(filename+" n'est pas une image")
                continue
            path = user + '/' + filename
            lable = id

            # Add to training data
            images.append(cv.imread(path, 0))
            lables.append(int(lable))
        id += 1

# Create a np array from the two lists above
(images, lables) = [np.array(lis) for lis in [images, lables]]

# Create LBP Face recoggnizer and save data
model = cv.face.LBPHFaceRecognizer_create()
model.train(images, lables)
model.write(data)
