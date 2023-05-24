import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from multiprocessing import Process

class OverlayWindow(QWidget):
    def __init__(self, text, timer=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.width = 200
        self.height = 100
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(100, 100, 200, 100)
        self.move((screen.width()-self.width)/2, (screen.height()-self.height)/2)
        
        self.label = QLabel(text, self)
        self.label.setStyleSheet("font-size: 20px; color: white;")
        self.label.setAlignment(Qt.AlignCenter)
        
        if timer:
            QTimer.singleShot(timer * 1000, QApplication.instance().quit)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            QApplication.quit()

def write_to_screen(text, timer):
    app = QApplication(sys.argv)
    window = OverlayWindow(text, timer)
    window.show()
    sys.exit(app.exec_())
    
def write_to_screen_process(text, timer):
    p = Process(target=write_to_screen, args=(text, timer))
    p.daemon = True
    p.start()