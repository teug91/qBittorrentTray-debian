#!./env/bin/python

import time
from qbittorrent import Client
# pylint: disable=no-name-in-module
from PySide2.QtCore import Signal, QThread
# pylint: enable=no-name-in-module


class Qbt(QThread):

    bad_settings = Signal()
    icon = Signal(str)
    delete_file = Signal(str)
    exit = Signal()

    def __init__(self, settings, torrent=None):
        super(Qbt, self).__init__()
        self._stop = False
        self._settings = settings
        self._torrent = torrent

    def run(self):
        self._authenticate()
        if not self._stop:
            if self._settings[3] or self._settings[5]:
                self.remove_check = True
            else:
                self.remove_check = False
            if self._torrent is not None:
                self.add_torrent(self._torrent)
            count = 0
            while not self._stop:
                self.icon.emit(self.torrents_running())
                if self.remove_check:
                    if count == 0:
                        count = 3
                        days = self._settings[3]
                        ratio = self._settings[4]
                        self.remove_torrents(days, ratio)
                    else:
                        count += 3
                time.sleep(3)

    def get_stop(self):
        return self._stop

    def stop(self):
        self._stop = True

    def remove_torrents(self, days, ratio):
        try:
            torrents = self._qb.torrents()
            if torrents is None:
                return
            if len(torrents) == 0:
                return
            hashes = list()

            if days:
                max_seed_time = int(self._settings[7]) * 86400
            if ratio:
                max_ratio = float(self._settings[6])

            for torrent in torrents:
                added = False
                torrent_hash = torrent["hash"]
                if days:
                    seed_time = int(self._qb.get_torrent(torrent_hash)["seeding_time"])
                    if seed_time > max_seed_time:
                        hashes.append(torrent_hash)
                        added = True
                if ratio:
                    torrent_ratio = float(torrent["ratio"])
                    if torrent_ratio > max_ratio:
                        if not added:
                            hashes.append(torrent["hash"])
            if len(hashes) != 0:
                if self._settings[5] == "Remove torrent and data":
                    self._qb.delete_permanently(hashes)
                elif self._settings[5] == "Remove torrent":
                    self._qb.delete(hashes)
        except Exception as e:
            print("remove check: failure")
            print(e)

    def add_torrent(self, torrent):
        if torrent.endswith(".torrent"):
            try:
                torrent_file = open(torrent, "rb")
                self._qb.download_from_file(torrent_file)
                if self._settings[8]:
                    self.delete_file.emit(torrent)
                if self._settings[9]:
                    self.exit.emit()
            except Exception as e:
                print("Failed to add torrent")
                print(torrent)
                print(e)
        elif torrent.startswith("magnet:?xt=urn:btih:"):
            try:
                self._qb.download_from_link(torrent)
                print("Added: " + torrent)
            except Exception as e:
                print("Failed to add torrent")
                print(torrent)
                print(e)

    def torrents_running(self):
        try:
            torrents = self._qb.torrents()
            if torrents is None:
                return None
            for torrent in torrents:
                state = torrent["state"]
                if state in ("pausedUP", "pausedDL"):
                    return "false"
        except:
            try:
                self._authenticate()
            except:
                print("relog failed")
            finally:
                return "dc"
        return "true"

    def toggle_states(self):
        try:
            if self.torrents_running() == "true":
                self._qb.pause_all()
            elif self.torrents_running() == "false":
                self._qb.resume_all()
        except:
            print("Toggling failed!")

    def _authenticate(self):
        authenticated = False
        credential_attempts = 0
        while not authenticated and not self._stop:
            try:
                self._qb = Client(self._settings[0])
                self._qb.login(self._settings[1], self._settings[2])
                self._qb.qbittorrent_version
                authenticated = True
                self.icon.emit("true")
            except Exception as e:
                exception_type = type(e).__name__
                print(exception_type)
                if exception_type in (
                    "MissingSchema",
                    "LoginRequired",
                    "AttributeError",
                ):
                    credential_attempts += 1
                    if credential_attempts > 1:
                        # self.stop_restart.emit()
                        self.bad_settings.emit()
                        self._stop = True
                        self.icon.emit("dc")
                else:
                    self.icon.emit("dc")
                    time.sleep(5)
