#delete.py
import sys, os
from shutil import rmtree

users_dir = 'Users'

try:
    user_name = input("Enter the name to delete \n")
except SyntaxError:
    print("Invalid name")
    sys.exit(0)
path = os.path.join(users_dir, user_name)
if not os.path.isdir(path):
    print("{0} not found in db".format(user_name))
    sys.exit(0)
for subdirs,dirs,files in os.walk(users_dir):
    for subdir in dirs:
        if subdir == user_name :
            rmtree(path)
            print("deleted {0}".format(user_name))
            break