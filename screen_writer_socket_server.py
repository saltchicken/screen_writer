import sys, time
import configargparse
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QTimerEvent

import socket, threading

class ServerThread(threading.Thread):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 12346))
        self.server_socket.listen(1)

    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print('Connection from', client_address)
            while True:
                try:
                    message = client_socket.recv(4096).decode()
                    self.label.setText(message)
                except Exception as e:
                    print(e)
                # finally:
                #     client_socket.close()

class OverlayWindow(QWidget):
    def __init__(self, args):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.width = args.width
        self.height = args.height
        self.screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, self.width, self.height)
        
        self.center_window()
        
        self.label = QLabel(self)
        self.label.setStyleSheet("font-size: 20px; color: white;")
        self.label.setGeometry(0, 0, self.width, self.height) 
        self.label.setAlignment(Qt.AlignCenter)
        
        self.start_server()
        

    def center_window(self):
        self.move(int((self.screen.width()-self.width)/2), int((self.screen.height()-self.height)/2))
        
    def start_server(self):
        self.server_thread = ServerThread(self.label)
        self.server_thread.start()
          
        

if __name__ == '__main__':
    parser = configargparse.ArgParser(default_config_files=['conf/server/default.ini'])
    parser.add('--width', type=int, required=True, help="Width of overlay")
    parser.add('--height', type=int, required=True, help="Height of overlay")
    args = parser.parse_args()
    print(args)
    app = QApplication([])
    window = OverlayWindow(args)
    window.label.setText('heh')
    window.show()
    sys.exit(app.exec_())