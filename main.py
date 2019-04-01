import sys
from PyQt5.QtWidgets import QApplication, QWidget , QLabel , QToolTip , QPushButton 
from PyQt5.QtWidgets import QMessageBox, QTextEdit, QGridLayout, QLineEdit,QInputDialog, QMainWindow, QAction,QFileDialog
from PyQt5.QtCore import QRegExp,pyqtSlot
from PyQt5.QtGui import QIcon, QFont, QTextDocument, QTextCursor
# from PyQt5.QtQuick import 
import os,re
from PyQt5 import QtCore

class MainW(QMainWindow):
    """docstring for ClassName"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.logApp=Logger(self)
        layout.addWidget(self.logApp,1,0,1,1)
        self.setGeometry(0, 0, 800, 480)
        self.setWindowTitle('Statusbar')    
        
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
         
        openButton = QAction(QIcon('exit24.png'), 'Open', self)
        openButton.setShortcut('Ctrl+O')
        openButton.setStatusTip('Open Log')
        openButton.triggered.connect(self.OpenFile)
        fileMenu.addAction(openButton)
        
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self.show()

    def OpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            Fr=open(fileName,"r")
            self.logApp.SourceDoc=QTextDocument(Fr.read())
            self.logApp.qTE.setDocument(self.logApp.SourceDoc)

class Logger(QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    def __init__(self,parent):
        super().__init__(parent)
        self.title = 'LogParser'
        self.setWindowIcon(QIcon('web.png'))
        self.left = parent.frameGeometry().left()
        self.top = parent.frameGeometry().top()+10
        self.width = parent.frameGeometry().width()
        self.height = parent.frameGeometry().height()
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

# class inputdialogdemo(QWidget):
#    def __init__(self, parent = Logger):
#       super(inputdialogdemo, self).__init__(parent)
        
#       layout = QFormLayout()

#       self.le = QLineEdit()
#       self.btn = QPushButton("Filter")
#       self.btn.clicked.connect(self.getFilter)  
#       layout.addRow(self.le,self.btn)
        
#    def getFilter(self):
#       items = ("C", "C++", "Java", "Python")
        
#       item, ok = QInputDialog.getItem(self, "select input dialog", 
#          "list of languages", items, 0, False)
            
#       if ok and item:
#          self.le.setText(item)
        

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MainW()
  sys.exit(app.exec_())
