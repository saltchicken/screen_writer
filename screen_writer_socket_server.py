import sys, json
import configargparse
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QStyle, QAction, QMenu, QSystemTrayIcon
from PyQt5.QtCore import Qt, QTimerEvent

import socket, threading
from loguru import logger

class ClientThread(threading.Thread):
    def __init__(self, label, quit_event):
        super().__init__()
        self.label = label
        self.quit_event = quit_event
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        server_address = '192.168.1.11'
        server_port = 9998
        logger.debug("Connecting to server")
        self.client_socket.connect((server_address, server_port))
        logger.debug("Connected to server")
        while not self.quit_event.is_set():
            try:
                data = self.client_socket.recv(4096).decode()
                packet = json.loads(data)
                if packet['type'] == 'phrase':
                    self.label.setText(packet['message'])
            except socket.timeout:
                logger.debug('Socket timeout')
                pass
        self.client_socket.close()

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
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setWordWrap(True)
        
        self.tray_menu = QMenu()
                
        self.clear_action_checkbox = QAction('Clear', self)
        self.clear_action_checkbox.setCheckable(True)
        self.clear_action_checkbox.triggered.connect(self.clear_action)
        self.tray_menu.addAction(self.clear_action_checkbox)
        
        self.quit_action_checkbox = QAction('Quit', self)
        self.quit_action_checkbox.setCheckable(True)
        self.quit_action_checkbox.triggered.connect(self.quit_action)
        self.tray_menu.addAction(self.quit_action_checkbox)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setToolTip("Tasker")
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        
        self.start_server()
        
    def center_window(self):
        self.move(int((self.screen.width()-self.width)/2), int((self.screen.height()-self.height)/2))
        
    def start_server(self):
        self.quit_event = threading.Event()
        self.server_thread = ClientThread(self.label, self.quit_event)
        self.server_thread.start()
                
    def quit_action(self):
        checked = self.quit_action_checkbox.isChecked()
        if checked:
            self.quit_event.set()
            QApplication.quit()
        else:
            print('This should have never been reached')
            
    def clear_action(self):
        checked = self.clear_action_checkbox.isChecked()
        if checked:
            self.label.setText('')
          
        

if __name__ == '__main__':
    parser = configargparse.ArgParser(default_config_files=['conf/server/default.ini'])
    parser.add('--width', type=int, required=True, help="Width of overlay")
    parser.add('--height', type=int, required=True, help="Height of overlay")
    args = parser.parse_args()
    print(args)
    app = QApplication([])
    window = OverlayWindow(args)
    # window.label.setText('Test')
    window.show()
    sys.exit(app.exec_())