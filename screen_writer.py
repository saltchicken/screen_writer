import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from multiprocessing import Process, Queue
        
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
        
    def event_loop(self):      
        try:
            message = self.queue.get_nowait()
            if message.type == 'write':
                self.label.setText(message.text)
            if message.type == 'append':
                self.label.setText(self.label.text() + message.text)
            if message.type == 'clear':
                self.label.setText('')
            if message.type == 'quit':
                QApplication.quit()
        except:
            time.sleep(0.25)

class CommandMessage():
    def __init__(self, type, text=None):
        self.type = type
        self.text = text
        
class OverlayController():
    def __init__(self, queue):
        self.queue = queue
        
    def write(self, text, timer=None):
        self.queue.put(CommandMessage('write', text))
        # TODO Figure out how to clear the label after a write with delay and be able to cancel if there is a new write
        # if timer:
        #     QTimer.singleShot(timer * 1000, self.clear)
        
    def append(self, text):
        self.queue.put(CommandMessage('append', text))
    
    def clear(self):
        self.queue.put(CommandMessage('clear'))
        
    def exit(self):
        self.queue.put(CommandMessage('quit'))
        
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
