import os, time

lastModified = dict()

marker = '>>>' 

targetDir = 'src'
refDir = 'ref'

def getLineReplacement(filename):
    for p, dir, files in os.walk(refDir):
        if filename not in files:
            continue
        path = os.path.join(p, filename)
        with open(path, 'r') as f:
            return f.read() + '\n'
    return "<<< Not Found\n"

def subMacros(path):
    substituted = False
    with open(path, 'r') as f:
        content = f.readlines()
        for ind, line in enumerate(content):
            i = line.find(marker)
            if i == -1:
                continue
            replacementFile = line[i+len(marker):].strip()
            content[ind] = getLineReplacement(replacementFile)
            substituted = True
    if not substituted:
        return
    with open(path, 'w') as f:
        f.writelines(content)
    print(path, 'has been substituted')
    
def getModifiedFiles():
    for p, dir, files in os.walk(targetDir):
        for filename in files:
            path = os.path.join(p, filename)
            modified = os.path.getmtime(path)
            if path in lastModified and lastModified[path] < modified:
                yield path
            lastModified[path] = modified

def watchFiles():
    while(True):
        modifiedFiles = getModifiedFiles()
        for filepath in modifiedFiles:
            subMacros(filepath)
        time.sleep(1)

if __name__ == '__main__':
    watchFiles()
