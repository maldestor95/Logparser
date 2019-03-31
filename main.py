import sys
from PyQt5.QtWidgets import QApplication, QWidget , QLabel , QToolTip , QPushButton , QMessageBox, QTextEdit, QFormLayout, QLineEdit,QInputDialog
from PyQt5.QtGui import QIcon, QFont, QTextDocument
import os

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'LogParser'
        self.setWindowIcon(QIcon('web.png'))
        self.left = 10
        self.top = 50
        self.width = 640
        self.height = 480
        self.openlog('t.log')
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        # self.SourceDoc=QTextDocument("")  
        self.qTE=QTextEdit(self)
        self.qTE.acceptDrops=True
        self.qTE.setGeometry(0, 0, self.frameGeometry().width(), self.frameGeometry().height()-100)
        self.qTE.setDocument(self.SourceDoc)
        self.qTE.show()

        self.setWindowTitle('Tooltips')    
        self.show()

        self.show()
        self.IDD=inputdialogdemo(self)
        self.IDD.show()
        
    def closeEvent(self, event):
        
        # reply = QMessageBox.question(self, 'Message',
        #     "Are you sure to quit?", QMessageBox.Yes | 
        #     QMessageBox.No, QMessageBox.No)

        # if reply == QMessageBox.Yes:
            event.accept()
        # else:
        #     event.ignore()
    def openlog(self,File_Path):
        if os.path.isfile(File_Path):
            Fr=open(File_Path,"r")
            self.SourceDoc=QTextDocument(Fr.read())

class inputdialogdemo(QWidget):
   def __init__(self, parent = App):
      super(inputdialogdemo, self).__init__(parent)
        
      layout = QFormLayout()

      self.le = QLineEdit()
      self.btn = QPushButton("Filter")
      self.btn.clicked.connect(self.getFilter)  
      layout.addRow(self.le,self.btn)
        
   def getFilter(self):
      items = ("C", "C++", "Java", "Python")
        
      item, ok = QInputDialog.getItem(self, "select input dialog", 
         "list of languages", items, 0, False)
            
      if ok and item:
         self.le.setText(item)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()


    sys.exit(app.exec_())