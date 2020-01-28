#!./env/bin/python

import os
import re
import sys


CONTROL = "/DEBIAN/control"
DESKTOP = "/usr/share/applications/qbittorrenttray.desktop"


def _main():
    current_path = _get_current_path()
    new_version = _get_version(_increment_version(current_path))
    new_path = f"qbittorrenttray_{new_version}"

    _remove("qbittorrenttray_*")
    _move(current_path, new_path)
    _set_version(f"{new_path}{CONTROL}", ": ", new_version)
    _set_version(f"{new_path}{DESKTOP}", "=", new_version)

    _pyinstall()
    _move("dist/qbittorrenttray", f"{new_path}/usr/local/bin/qbittorrenttray")
    _package(new_path)


def _get_current_path():
    folder_content = os.listdir(".")
    regex_pattern = "qbittorrenttray_[0-9]+.[0-9]+$"
    regex = re.compile(regex_pattern)
    for path in folder_content:
        if regex.search(path):
            return path
    print("Package directory not found")
    exit()


def _increment_version(path):
    version = path.split("_")[1]
    versions = version.split(".")
    return f"{versions[0]}.{int(versions[1]) + 1}"


def _get_version(default):
    while True:
        answer = input(f"Enter version (default = {default}): ")
        if answer == "":
            return default
        pattern = re.compile("[0-9]+.[0-9]+$")
        if pattern.match(answer):
            return answer


def _set_version(path, seperator, version):
    file_handle = open(path, "r")
    file_string = file_handle.read()
    file_handle.close()

    regex_pattern = f"Version{seperator}[0-9]+.[0-9]+"
    replacement = f"Version{seperator}{version}"
    file_string = re.sub(regex_pattern, replacement, file_string)

    file_handle = open(path, "w")
    file_handle.write(file_string)
    file_handle.close()


def _pyinstall():
    os.system("pyinstaller qbittorrenttray.spec")


def _move(current, new):
    os.system(f"mv {current} {new}")


def _remove(path):
    os.system(f"rm {path}")


def _package(path):
    os.system(f"dpkg-deb --build {path}")


if __name__ == "__main__":
    _main()
