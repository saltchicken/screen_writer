import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer

class OverlayWindow(QWidget):
    def __init__(self, text, timer=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 200, 100)
        
        self.label = QLabel(text, self)
        self.label.setStyleSheet("font-size: 20px; color: white;")
        self.label.setAlignment(Qt.AlignCenter)
        
        if timer:
            QTimer.singleShot(timer * 1000, QApplication.instance().quit)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            QApplication.quit()

def writeToScreen(text, timer):
    app = QApplication(sys.argv)
    window = OverlayWindow(text, timer)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    writeToScreen('test', 5)