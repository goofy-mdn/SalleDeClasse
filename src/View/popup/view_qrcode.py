from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QImage

import pyqrcode
import socket
from subprocess import check_output

from src.assets_manager import AssetManager

QR_PATH = 'assets/qr.png'


class VQRCode(QDialog):

    def __init__(self, parent):
        """
        Confirm dialog for dangerous actions

        :param parent: gui's main window
        """
        QDialog.__init__(self, parent)

        # QR Code
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # This will require an internet connection
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets

        # IP and Port
        local_ip_address = s.getsockname()[0]
        s.close()
        port = AssetManager.getInstance().config('webapp', 'port')

        s = f"http://{local_ip_address}:{port}"  # String which represents the QR code
        self.url = pyqrcode.create(s)  # Generate QR code
        self.url.png(QR_PATH, scale=6)  # Create and save the QR png file

        # Widgets
        self.qr = QLabel()  # Label that contains the QR
        pix = QPixmap(QImage(QR_PATH))
        self.qr.setPixmap(pix)

        # Layout
        layout = QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.qr)
        layout.setAlignment(self.qr, Qt.AlignCenter)
        self.setLayout(layout)