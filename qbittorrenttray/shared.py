#!./env/bin/python

import sys, os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS # pylint: disable=no-member
    except Exception:
        print('not meipass')
        base_path = os.path.abspath("./qbittorrenttray/resources")

    return os.path.join(base_path, relative_path)
