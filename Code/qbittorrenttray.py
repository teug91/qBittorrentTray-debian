#!/usr/bin/python

import sys
import os
import subprocess
from PySide2.QtWidgets import QApplication, QDialog
from tray import TrayIcon
from settings_manager import SettingsManager
from settings_window import Settings_Window
from qbt import Qbt
from qtsingleapplication import QtSingleApplication


class Application:
    def __init__(self):
        self._env = self._get_env()
        self._app = QtSingleApplication()
        self._app.messageReceived.connect(self._add_torrent)
        torrent = self._get_torrent(sys.argv)
        if self._app.is_running():
            if torrent:
                self._app.send_message(torrent)
            sys.exit(0)
        self._new_settings = True
        self._status = "dc"
        self._app.setQuitOnLastWindowClosed(False)
        self._settings_man = SettingsManager()
        self._settings_values = self._settings_man.get_settings()
        self._tray = TrayIcon(self._app)
        self._tray.settings_clicked.connect(self._open_settings)
        self._tray.toggle_clicked.connect(self._toggle_state)
        self._tray.webui_clicked.connect(self._webui)
        self._tray.exit_clicked.connect(sys.exit)
        self._start_qbt_thread(self._settings_values, torrent)
        sys.exit(self._app.exec_())

    def _icon(self, value):
        if self._status != value:
            self._status = value
            if value == "dc":
                self._tray.set_dc()
            elif value == "false":
                self._tray.set_pause()
            elif value == "true":
                self._tray.set_qb()

    def _save(self, values):
        self._settings_man.save_settings(values)
        self._settings_values = values
        self._new_settings = True
        try:
            if not self._qbt_thread.isRunning():
                self._start_qbt_thread(self._settings_values)
            elif not self._qbt_thread.get_stop():
                self._qbt_thread.stop()
        except Exception as e:
            print("Unable to check thread")
            print(e)
            self._start_qbt_thread(self._settings_values)

    def _restart_qbt_thread(self):
        self._start_qbt_thread(self._settings_values)

    def _start_qbt_thread(self, settings, torrents=None):
        if not self._new_settings:
            return
        self._new_settings = False
        self._qbt_thread = Qbt(settings, torrents)
        self._qbt_thread.icon.connect(self._icon)
        self._qbt_thread.bad_settings.connect(self._open_settings)
        self._qbt_thread.delete_file.connect(self._delete_file)
        self._qbt_thread.finished.connect(self._restart_qbt_thread)
        self._qbt_thread.exit.connect(self._exit)
        self._qbt_thread.start()

    def _open_settings(self):
        self._window = Settings_Window(self._settings_values)
        self._window.save_clicked.connect(self._save)

    def _toggle_state(self):
        try:
            self._qbt_thread.toggle_states()
        except:
            pass

    def _webui(self):
        try:
            subprocess.Popen(["xdg-open", self._settings_values[0]], env=self._env)
        except:
            pass

    def _add_torrent(self, value):
        try:
            print("Adding: " + value)
            self._qbt_thread.add_torrent(value)
            print("Post add")
        except:
            pass

    @staticmethod
    def _delete_file(value):
        os.remove(value)

    @staticmethod
    def _exit():
        sys.exit(0)

    @staticmethod
    def _get_torrent(args):
        for arg in args:
            if arg.endswith(".torrent") or arg.startswith("magnet:?xt=urn:btih:"):
                return arg
        return None

    @staticmethod
    def _get_env():
        env = dict(os.environ)
        lp_key = "LD_LIBRARY_PATH"
        lp_orig = env.get(lp_key + "_ORIG")
        if lp_orig is not None:
            env[lp_key] = lp_orig
        else:
            lp = env.get(lp_key)
            if lp is not None:
                env.pop(lp_key)
        return env


if __name__ == "__main__":
    Application()
