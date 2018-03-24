
import os

def removeFile(f):
    if os.path.exists(f):
        os.remove(f)