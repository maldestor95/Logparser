import sys
from PyQt5.QtWidgets import QApplication, QWidget , QLabel
from PyQt5.QtGui import QIcon
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
     
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.se
        label=QLabel(self)
        label.setText("toto")
        # label.setStyle()
        label.show()
        z = QWidget(self)
        z.resize(250, 150)
        z.move(400, 300)
        z.setWindowTitle('SimpleZ')
        z.show()


        self.show()
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()


    sys.exit(app.exec_())