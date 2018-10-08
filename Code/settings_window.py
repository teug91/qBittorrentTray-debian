#!/usr/bin/python

from shared import resource_path
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication, QFormLayout, QVBoxLayout, QGridLayout, QDialog, QComboBox, QLabel, QCheckBox, QPushButton, QSizePolicy, QGroupBox)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal, Qt

class Settings_Window(QDialog):

    save_clicked = Signal(list)

    def __init__(self, values):
        super(Settings_Window, self).__init__(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        self._host = QLineEdit(values[0])
        self._host.setToolTip("Example: http://192.168.1.100:8080")
        self._username = QLineEdit(values[1])
        self._username.setToolTip("WebUI username")
        self._password = QLineEdit(values[2])
        self._password.setEchoMode(QLineEdit.Password)
        self._password.setToolTip("WebUI password")

        _form_layout = QFormLayout()
        _form_layout.addRow("Host:", self._host)
        _form_layout.addRow("Username:", self._username)
        _form_layout.addRow("Password:", self._password)

        _grid_layout = QGridLayout()
        _grid_layout.setColumnMinimumWidth(4, 0)
        _grid_layout.setColumnStretch(4, 1)

        self._ratio_box = QCheckBox("Seed torrents until their ratio exceeds")
        self._ratio_box.setChecked(values[3] == "true")
        self._ratio_box.stateChanged.connect(self._removal_visibility)
        _grid_layout.addWidget(self._ratio_box, 0, 0)
        self._ratio = QComboBox()
        self._ratio.addItems(["{0:.1f}".format(round(x, 1)) for x in list(self._drange(0, 9.9, 0.1))])
        self._ratio.setCurrentText(values[6])
        self._ratio.setDisabled(True)
        self._ratio.setToolTip("Upload/download ratio")
        _grid_layout.addWidget(self._ratio, 0, 1)

        self._days_box = QCheckBox("Seed torrents until their seeding time exceeds")
        self._days_box.setChecked(values[4] == "true")
        self._days_box.stateChanged.connect(self._removal_visibility)
        _grid_layout.addWidget(self._days_box, 1, 0)
        self._days = QComboBox()
        self._days.addItems([format(x) for x in list(range(100))])
        self._days.setCurrentText(values[7])
        self._days.setDisabled(True)
        _grid_layout.addWidget(self._days, 1, 1)
        _grid_layout.addWidget(QLabel("days"), 1, 2)

        _grid_layout.addWidget(QLabel("then"), 2, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        self._remove_action = QComboBox()
        self._remove_action.addItems(["Remove torrent", "Remove torrent and data"])
        self._remove_action.setCurrentText(values[5])
        self._remove_action.setDisabled(True)
        _grid_layout.addWidget(self._remove_action, 2, 1, 1, 3)

        _group_box = QGroupBox("Seed limiting")
        _group_box.setLayout(_grid_layout)

        _bottom_grid_layout = QGridLayout()
        _bottom_grid_layout.setRowMinimumHeight(0, 30)
        _bottom_grid_layout.setColumnMinimumWidth(1, 100)
        _bottom_grid_layout.setColumnStretch(1, 1)

        self._delete_torrent_box = QCheckBox("Delete .torrent after torrent is added")
        self._delete_torrent_box.setChecked(values[8] == "true")
        self._delete_torrent_box.setToolTip("Delete .torrent after attempting to add .torrent")
        _bottom_grid_layout.addWidget(self._delete_torrent_box, 1, 0)
        _save_button = QPushButton("Save")
        _save_button.clicked.connect(self._save_click)
        _bottom_grid_layout.addWidget(_save_button, 1, 2)
        _cancel_button = QPushButton("Cancel")
        _cancel_button.clicked.connect(self._cancel_click)
        _bottom_grid_layout.addWidget(_cancel_button, 1, 3)


        _main_layout = QVBoxLayout()
        _main_layout.addLayout(_form_layout)
        space = QGridLayout()
        space.setRowMinimumHeight(0, 30)
        _main_layout.addStretch(1)
        _main_layout.addLayout(space)
        _main_layout.addWidget(_group_box)
        _main_layout.addLayout(_bottom_grid_layout)

        self.setLayout(_main_layout)

        self.setWindowIcon(QIcon(resource_path("qbdark_big.png")))
        self.setWindowTitle("qBittorrentTray settings")
        self._removal_visibility()
        self.show()

    def _cancel_click(self):
        self.hide()
        self.close()

    def _save_click(self):
        values = [self._host.text(), self._username.text(), self._password.text(), self._ratio_box.isChecked(), 
            self._days_box.isChecked(), self._remove_action.currentText(), self._ratio.currentText(), 
            self._days.currentText(), self._delete_torrent_box.isChecked(), False]
        self.save_clicked.emit(values)
        self.hide()
        self.close()

    def _removal_visibility(self):
        ratio_checked = self._ratio_box.isChecked()
        days_checked = self._days_box.isChecked()
        either_checked = ratio_checked or days_checked
        ratio_enabled = self._ratio.isEnabled()
        days_enabled = self._days.isEnabled()
        action_enabled = self._remove_action.isEnabled()
        if ratio_checked is not ratio_enabled:
            self._ratio.setEnabled(ratio_checked)
        if days_checked is not days_enabled:
            self._days.setEnabled(days_checked)
        if either_checked is not action_enabled:
            self._remove_action.setEnabled(either_checked)

    def _drange(self, start, end, step):
        i = start
        while i < end:
            yield i
            i += step
