import sys
from PyQt5.QtWidgets import QApplication, QWidget , QLabel , QToolTip , QPushButton , QMessageBox
from PyQt5.QtGui import QIcon, QFont
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'LogParser'
        self.setWindowIcon(QIcon('web.png'))
        self.left = 10
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()
     
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.se

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QPushButton('Button', self)
        # QPushButton(string text, QWidget parent = None)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)  
             
        
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(100, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')    
        self.show()


        self.show()

    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()


    sys.exit(app.exec_())