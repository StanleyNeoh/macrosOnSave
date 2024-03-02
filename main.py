import os, time, json

macro_config_filename = 'macro_config.json'
marker = '>>>' 
last_modified = dict()
watch_dir = None
macro_dir = None

def get_line_replacement(filename):
    for p, dir, files in os.walk(macro_dir):
        for name in files:
            if filename not in name:
                continue
            path = os.path.join(p, name)
            with open(path, 'r') as f:
                return f.read() + '\n'
    return "<<< Not Found\n"

def substitute_macros(path):
    substituted = False
    with open(path, 'r') as f:
        content = f.readlines()
        for ind, line in enumerate(content):
            i = line.find(marker)
            if i == -1:
                continue
            replacementFile = line[i+len(marker):].strip()
            content[ind] = get_line_replacement(replacementFile)
            substituted = True
    if not substituted:
        return
    with open(path, 'w') as f:
        f.writelines(content)
    print(path, 'has been substituted')
    
def get_modified_files():
    for p, dir, files in os.walk(watch_dir):
        for filename in files:
            path = os.path.join(p, filename)
            modified = os.path.getmtime(path)
            if path in last_modified and last_modified[path] < modified:
                yield path
            last_modified[path] = modified

def watch_files():
    while(True):
        modified_files = get_modified_files()
        for filepath in modified_files:
            substitute_macros(filepath)
        time.sleep(1)

def start():
    if not os.path.exists(macro_config_filename):
        with open(macro_config_filename, 'w') as f:
            f.write(json.dumps({
                'watch_dir': 'src/',
                'macro_dir': 'macros/'
            }, indent=2))
        print(f"Creating new {macro_config_filename}. Please edit the file to your requirements before re-running")
        return
        
    global watch_dir, macro_dir
    with open(macro_config_filename) as f:
        config = json.load(f)
        watch_dir = config['watch_dir']
        macro_dir = config['macro_dir']
    
    if not os.path.exists(watch_dir):
        print(f"{watch_dir} does not exist, please create the directory or update {macro_config_filename}")
        return
    if not os.path.exists(macro_dir):
        print(f"{macro_dir} does not exist, please create the directory or update {macro_config_filename}")
        return
    print(f"Watching files in {watch_dir}")
    watch_files()
    print(f"Stopping macros")

if __name__ == '__main__':
    start()
