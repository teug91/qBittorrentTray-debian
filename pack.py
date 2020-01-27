#!./env/bin/python

import os, re, sys

def main():
    version = get_version()
    current_path = get_current_path()
    new_path = 'qbittorrenttray_' + version
    os.rename(current_path, new_path)
    build(new_path)

def get_version():
    if len(sys.argv) == 1:
        print('Version argument is missing')
        exit()
    return sys.argv[1]

def get_current_path():
    folder_content = os.listdir('.')
    regex_pattern = 'qbittorrenttray_*[0-9]*.[0-9]*.[0-9]*$'
    regex = re.compile(regex_pattern)
    for path in folder_content:
        if regex.search(path):
            return path
    print('Package directory not found')
    exit()

def build(path):
    os.system('pyinstaller qbittorrenttray.spec')
    os.system('mv dist/qbittorrenttray ' + path + '/usr/local/bin/qbittorrenttray')
    os.system('dpkg-deb --build ' + path)

if __name__ == '__main__':
    main()
