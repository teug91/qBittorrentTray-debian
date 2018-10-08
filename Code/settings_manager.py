#!/usr/bin/python

import base64
from PySide2.QtCore import (Signal, QSettings, QObject)

class SettingsManager(QObject):

    def __init__(self):
        super(SettingsManager, self).__init__()
        self._settings = QSettings("/etc/qBittorrentTray/config.ini", QSettings.IniFormat)

    def get_settings(self):
        try:
            if self._settings.value("host"):
                settings = [self._settings.value("host"), self._settings.value("username"), self._settings.value("password"), 
                    self._settings.value("remove_ratio"), self._settings.value("remove_days"), self._settings.value("remove_action"), 
                    self._settings.value("ratio"), self._settings.value("days"), self._settings.value("delete"), self._settings.value("autorun")]
                if settings[2]:
                    settings[2] = base64.b64decode(settings[2])
                return settings
            return self._default_settings()
        except Exception as e:
            print("failed to get settings")
            print(e)
            return self._default_settings()

    def save_settings(self, values):
        self._settings.setValue("host", values[0])
        self._settings.setValue("username", values[1])
        self._settings.setValue("password", base64.b64encode(values[2].encode()))
        self._settings.setValue("remove_ratio", values[3])
        self._settings.setValue("remove_days", values[4])
        self._settings.setValue("remove_action", values[5])
        self._settings.setValue("ratio", values[6])
        self._settings.setValue("days", values[7])
        self._settings.setValue("delete", values[8])
        self._settings.setValue("autorun", values[9])

    def _default_settings(self):
        self._settings.setValue("host", "")
        self._settings.setValue("username", "")
        self._settings.setValue("password", "")
        self._settings.setValue("remove_ratio", "false")
        self._settings.setValue("remove_days", "false")
        self._settings.setValue("remove_action", "Remove torrent")
        self._settings.setValue("ratio", "1.1")
        self._settings.setValue("days", "15")
        self._settings.setValue("delete", "false")
        self._settings.setValue("autorun", "false")
        return ["", "", "", "false", "false", "Remove torrent", "1.1", "15", "false", "false"]
