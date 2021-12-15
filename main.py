import pathlib
import sys

import cv2
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFileDialog, QInputDialog, \
    QLineEdit, QMessageBox, QGridLayout
from matplotlib import pyplot as plt

from detect2 import  detect

import os.path as osp




#-------------------------------------------------------------------------------------------------------------------

images = "";
nms = "0.4";
confidence = "0.5";




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 textbox - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox_nms = QLineEdit(self)
        global nms
        self.textbox_nms.setText(nms)
        self.textbox_nms.resize(40, 40)

        self.textbox_confidence = QLineEdit(self)
        global confidence
        self.textbox_confidence.setText(confidence)
        self.textbox_confidence.resize(40, 40)

        #
        self.btn = QPushButton("Open File")
        self.start = QPushButton("start")

        # Create a button in the window
        self.btn_nms = QPushButton('change nms', self)
        self.btn_confidence = QPushButton('change confidence', self)

        # connect button to function on_click
        self.btn_nms.clicked.connect(self.on_click_nms)
        self.btn_confidence.clicked.connect(self.on_click_confidence)
        self.btn.clicked.connect(self.open)
        self.start.clicked.connect(self.startDetect)

        #addWidget(*Widget, row, column, rowspan, colspan)
        layout = QGridLayout();
        layout.addWidget(self.btn, 0, 0)
        layout.addWidget(self.textbox_nms, 1, 0)
        layout.addWidget(self.btn_nms, 1, 1)

        layout.addWidget(self.textbox_confidence, 2, 0)
        layout.addWidget(self.btn_confidence, 2, 1)

        layout.addWidget(self.start, 5, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.show()

    def on_click_nms(self):
        global nms
        nms = self.textbox_nms.text()
        QMessageBox.question(self, '', "nms: " + nms, QMessageBox.Ok, QMessageBox.Ok)

    def on_click_confidence(self):
        global confidence
        confidence = self.textbox_confidence.text()
        QMessageBox.question(self, '', "confidence: " + confidence, QMessageBox.Ok, QMessageBox.Ok)

    def startDetect(self):
        detect(images, float(nms), float(confidence))

    def open(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'All Files (*.*)')
        if path != ('', ''):
            local = str(pathlib.Path().resolve())
            x = local.split('\\')
            y = path[0].split(x[len(x) - 1])
            global images
            images = "." + y[1]
            #print(str(osp.realpath('.')))
            #print(images)
            join = osp.join(osp.realpath('.'), images)
            print(join)
            print(type(join))
            img = cv2.imread(osp.join(osp.realpath('.'), images))
            cv2.imshow('image window', img)
            # add wait key. window waits until user presses a key
            cv2.waitKey(0)
            # and finally destroy/close all open windows
            cv2.destroyAllWindows()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
