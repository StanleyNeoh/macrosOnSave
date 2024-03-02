import os, time

lastModified = dict()

def getModifiedFiles():
    for p, dir, files in os.walk('src'):
        for f in files:
            path = os.path.join(p, f)
            modified = os.path.getmtime(path)
            if path in lastModified and lastModified[path] < modified:
                yield path
            lastModified[path] = modified

def watchFiles():
    while(True):
        modifiedFiles = getModifiedFiles()
        for x in modifiedFiles:
            print(x)
        time.sleep(1)

if __name__ == '__main__':
    watchFiles()

