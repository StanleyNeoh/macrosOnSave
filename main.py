import os, time, json

last_modified = dict()
macro_config_filename = 'macro_config.json'

marker = None
watch_dir = None
macro_dir = None
replace_start = None
replace_end = None
refresh_time = None

def get_line_replacement(filename):
    if not filename:
        return '<<< Empty name\n'
    for p, dir, files in os.walk(macro_dir):
        for name in files:
            if filename not in name:
                continue
            path = os.path.join(p, name)
            with open(path, 'r') as f:
                macroStart = False
                lines = []
                for l in f.readlines():
                    if replace_start in l:
                        macroStart = True
                    elif not macroStart:
                        continue
                    elif replace_end in l:
                        break
                    else:
                        lines.append(l)
                return ''.join(lines) + '\n'
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
        time.sleep(0.3)

def start():
    if not os.path.exists(macro_config_filename):
        with open(macro_config_filename, 'w') as f:
            f.write(json.dumps({
                'watch_dir': 'src/',
                'macro_dir': 'macros/',
                'marker': '>>>',
                'replace_start': 'MACRO-START',
                'replace_end': 'MACRO-END',
                'refresh_time': 0.3,
            }, indent=2))
        print(f"Creating new {macro_config_filename}. Please edit the file to your requirements before re-running")
        return
        
    global watch_dir, macro_dir, marker, replace_start, replace_end, refresh_time
    with open(macro_config_filename) as f:
        config = json.load(f)
        watch_dir = config['watch_dir']
        macro_dir = config['macro_dir']
        marker = config['marker']
        replace_start = config['replace_start']
        replace_end = config['replace_end']
        refresh_time = config['refresh_time']
    
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
