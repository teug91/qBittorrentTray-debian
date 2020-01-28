#!./env/bin/python

########################################################################################################################################################
#   From user user763305, Stackoverflow. See https://stackoverflow.com/questions/12712360/qtsingleapplication-for-pyside-or-pyqt
#
#   Note: This license has also been called the "Simplified BSD License" and the "FreeBSD License". See also the 3-clause BSD License.
#
#   Copyright <YEAR> <COPYRIGHT HOLDER>
#
#   Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#   INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY
#   OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
#   OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################################################################################################

from PySide2.QtNetwork import QLocalSocket, QLocalServer
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Signal, QTextStream


class QtSingleApplication(QApplication):

    messageReceived = Signal(str)

    def __init__(self):
        super(QtSingleApplication, self).__init__()
        self._id = "/etc/qbittorrenttray/socket"

        # Is there another instance running?
        self._out_socket = QLocalSocket()
        self._out_socket.connectToServer(self._id)
        self._is_running = self._out_socket.waitForConnected()

        if self._is_running:
            # Yes, there is.
            self._out_stream = QTextStream(self._out_socket)
            self._out_stream.setCodec("UTF-8")
        else:
            # No, there isn't.
            self._out_socket = None
            self._out_stream = None
            self._in_socket = None
            self._in_stream = None
            QLocalServer.removeServer(self._id)
            self._server = QLocalServer()
            self._server.listen(self._id)
            self._server.newConnection.connect(self._on_new_connection)

    def is_running(self):
        return self._is_running

    def send_message(self, msg):
        if not self._out_stream:
            return False
        self._out_stream << msg << "\n"
        self._out_stream.flush()
        return self._out_socket.waitForBytesWritten()

    def _on_new_connection(self):
        if self._in_socket:
            self._in_socket.readyRead.disconnect(self._on_ready_read)
        self._in_socket = self._server.nextPendingConnection()
        if not self._in_socket:
            return
        self._in_stream = QTextStream(self._in_socket)
        self._in_stream.setCodec("UTF-8")
        self._in_socket.readyRead.connect(self._on_ready_read)

    def _on_ready_read(self):
        while True:
            msg = self._in_stream.readLine()
            if not msg:
                break
            self.messageReceived.emit(msg)
