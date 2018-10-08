#!/usr/bin/python

#import sys, os
from shared import resource_path
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QDialog
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal

class TrayIcon(QSystemTrayIcon):

    settings_clicked = Signal()
    toggle_clicked = Signal()
    webui_clicked = Signal()
    exit_clicked = Signal()

    def __init__(self, parentApp):
        self._icon_qb = QIcon(resource_path("qbdark_big.png"))
        self._icon_pause = QIcon(resource_path("qbdark_pause_big.png"))
        self._icon_dc = QIcon(resource_path("qbdark_dc_big.png"))
        super(TrayIcon, self).__init__(self._icon_dc, parent=parentApp)
        self.setToolTip("qBittorrentTray")
        menu = QMenu()
        toggle_action = menu.addAction("Start/pause")
        toggle_action.triggered.connect(self._emit_toggle)
        webui_action = menu.addAction("WebUI")
        webui_action.triggered.connect(self._emit_webui)
        setting_action = menu.addAction("Settings")
        setting_action.triggered.connect(self._emit_settings)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self._emit_exit)
        self.setContextMenu(menu)
        self.show()

    def _emit_settings(self):
        self.settings_clicked.emit()

    def _emit_toggle(self):
        self.toggle_clicked.emit()

    def _emit_webui(self):
        self.webui_clicked.emit()

    def _emit_exit(self):
        self.exit_clicked.emit()

    def set_qb(self):
        self.setIcon(self._icon_qb)

    def set_pause(self):
        self.setIcon(self._icon_pause)

    def set_dc(self):
        self.setIcon(self._icon_dc)
