#!./env/bin/python

import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        print("not meipass")
        base_path = os.path.abspath("./qbittorrenttray/resources")

    return os.path.join(base_path, relative_path)
