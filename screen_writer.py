import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from multiprocessing import Process, Queue
import time
        
class OverlayWindow(QWidget):
    def __init__(self, text, timer=None, queue=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.width = 800
        self.height = 100
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, self.width, self.height)
        self.move(int((screen.width()-self.width)/2), int((screen.height()-self.height)/2))
        
        self.label = QLabel(text, self)
        self.label.setText(text)
        self.label.setStyleSheet("font-size: 20px; color: white;")
        self.label.setGeometry(0, 0, self.width, self.height) 
        self.label.setAlignment(Qt.AlignCenter)
        
        if queue:
            self.queue = queue
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.event_loop)
            self.timer.start()
        
        if timer:
            QTimer.singleShot(timer * 1000, QApplication.instance().quit)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            QApplication.quit()
                       
    def event_loop(self):      
        try:
            message = self.queue.get_nowait()
            self.label.setText(message)
        except:
            time.sleep(0.25)

class OverlayController():
    def __init__(self, queue):
        self.queue = queue
        
    def write(self, text):
        # TODO Make this a JSON object with write type
        self.queue.put(text)
        
    def exit(self):
        # TODO Make this a JSON object with command type
        self.queue.put('exit')
        
def write_to_screen_process(text, timer, queue=None):
    app = QApplication(sys.argv)
    window = OverlayWindow(text, timer, queue)
    window.show()
    sys.exit(app.exec_())
    
def write_to_screen(text, timer, queue=False):
    if queue:
        queue = Queue()
        p = Process(target=write_to_screen_process, args=(text, timer, queue))
        p.daemon = True
        p.start()
        return OverlayController(queue)
    else:
        p = Process(target=write_to_screen_process, args=(text, timer))
        p.daemon = True
        p.start()