import sys
from PyQt5.QtWidgets import QApplication, QWidget , QLabel , QToolTip , QPushButton , QMessageBox, QTextEdit, QGridLayout, QLineEdit,QInputDialog
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon, QFont, QTextDocument, QTextCursor
import os,re
from PyQt5 import QtCore

class App(QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
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
        self.keyPressed.connect(self.on_key)
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        # self.SourceDoc=QTextDocument("")  
        layout = QGridLayout()
        
        self.le = QLineEdit()
        self.btn = QPushButton("Filter")
  
        self.btn.clicked.connect(self.getFilter)  
        layout.addWidget(self.le,0,0)
        layout.addWidget(self.btn,0,1)
          
        self.qTE=QTextEdit(self)
        layout.addWidget(self.qTE,1,0,3,2)  
        
        self.qTEout=QTextEdit(self)
        layout.addWidget(self.qTEout,4,0,3,2)  

        self.setLayout(layout)
        self.qTE.acceptDrops=True
        self.qTE.setDocument(self.SourceDoc)


        self.setWindowTitle('Tooltips')    
        self.show()


    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.keyPressed.emit(event) 

    def on_key(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            self.getFilter()  # this is called whenever the continue button is pressed
        elif event.key() == QtCore.Qt.Key_Q:
            print("Killing")
            self.deleteLater()  # a test I implemented to see if pressing 'Q' would close the window

    def getFilter_old(self):  
      """ negate filter """
      tt=QTextDocument(self.le.text())
      # lRe=QRegExp("^((?!look).)*$")#self.le.text())
      print("^((?!{0}).)*$".format(tt.toPlainText()))
      lRe=QRegExp("^((?!{0}).)*$".format(tt.toPlainText()))#self.le.text())
      lDoc=QTextDocument(self.qTE.document().toPlainText())

      # ^.+?(?=look)  jusqu'au mot look
      # ^((?!look).)*$   lines not containing look

      lCursor=lDoc.find(lRe)
      EndDocCursor=QTextCursor(lDoc)
      EndDocCursor.movePosition(QTextCursor.End)
      EndDocCursorPos=EndDocCursor.position()


      while lCursor.position()< EndDocCursorPos :
        lCursor.movePosition(QTextCursor.NextBlock,QTextCursor.KeepAnchor)
        lCursor.removeSelectedText();
        lCursor=lDoc.find(lRe)
        EndDocCursor.movePosition(QTextCursor.End)
        EndDocCursorPos=EndDocCursor.position()

      self.qTEout.setDocument(lDoc)
    
    def getFilter(self):
      """ positive filter"""
      tt=QTextDocument(self.le.text())
      # lRe=QRegExp("^((?!look).)*$")#self.le.text())
      # print("{0}".format(tt.toPlainText()))
      lRe=QRegExp("{0}".format(tt.toPlainText()))#self.le.text())
      lDoc=QTextDocument(self.qTE.document().toPlainText())

      # ^.+?(?=look)  jusqu'au mot look
      # ^((?!look).)*$   lines not containing look

      # lCursor=lDoc.find(lRe)
      EditCursor=QTextCursor(lDoc)
      
      #Remove first REgex
      lCursor=lDoc.find(lRe)
      EditCursor.setPosition(lCursor.position(),QTextCursor.KeepAnchor)
      EditCursor.movePosition(QTextCursor.EndOfLine,QTextCursor.KeepAnchor)
      EndLine=EditCursor.position()
      EditCursor.movePosition(QTextCursor.StartOfLine,QTextCursor.KeepAnchor)
      StartLine=EditCursor.position()
      # print("step1 :", lCursor.position(),EditCursor.anchor(),EditCursor.position())
      EditCursor.removeSelectedText();

      #Remove other Regex
      StartPos=EndLine-StartLine+1
      # print("StartPos ",StartPos)
      lCursor=lDoc.find(lRe,StartPos)
      EditCursor.setPosition(StartPos)
      while lCursor.position()>0:

        EditCursor.setPosition(lCursor.position(),QTextCursor.KeepAnchor)
        EditCursor.movePosition(QTextCursor.EndOfLine,QTextCursor.KeepAnchor)
        EndLine=EditCursor.position()
        EditCursor.movePosition(QTextCursor.StartOfLine,QTextCursor.KeepAnchor)
        StartLine=EditCursor.position()
        
        # print("step2 :", lCursor.position(),EditCursor.anchor(),EditCursor.position())
        EditCursor.removeSelectedText();

        StartPos=EndLine-StartLine +1+StartPos
        # print("StartPos ",StartPos)
        lCursor=lDoc.find(lRe,StartPos)
        EditCursor.setPosition(StartPos)
        # print(lCursor.position())
      
      # remove after regex
      EditCursor.setPosition(StartPos)
      EditCursor.movePosition(QTextCursor.End,QTextCursor.KeepAnchor)
      # print(EditCursor.position(), EditCursor.anchor())
      EditCursor.removeSelectedText();

      self.qTEout.setDocument(lDoc)
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
  sys.exit(app.exec_())