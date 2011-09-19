import os
import fnmatch 

def locate_files(directory, pattern, followlinks=True):
    for root, dirs, files in os.walk(directory, followlinks=followlinks): #@UnusedVariable
        for f in files: 
            if fnmatch.fnmatch(f, pattern):
                yield os.path.join(root, f)

