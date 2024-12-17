import os

def delete_Recording(savedDirectory):
    if os.path.exists(savedDirectory):
        os.remove(savedDirectory)