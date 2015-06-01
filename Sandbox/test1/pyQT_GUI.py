# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface1.ui'
#
# Created: Mon May  4 11:53:19 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1057, 620)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1057, 620))
        MainWindow.setMaximumSize(QtCore.QSize(1057, 620))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 251, 561))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.msgPanel = QtGui.QTextEdit(self.frame)
        self.msgPanel.setGeometry(QtCore.QRect(10, 10, 231, 541))
        self.msgPanel.setObjectName(_fromUtf8("msgPanel"))
        self.vtkFrame = QtGui.QFrame(self.centralwidget)
        self.vtkFrame.setGeometry(QtCore.QRect(270, 10, 771, 491))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vtkFrame.sizePolicy().hasHeightForWidth())
        self.vtkFrame.setSizePolicy(sizePolicy)
        self.vtkFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.vtkFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.vtkFrame.setObjectName(_fromUtf8("vtkFrame"))
        self.controlFrame = QtGui.QFrame(self.centralwidget)
        self.controlFrame.setGeometry(QtCore.QRect(270, 510, 771, 61))
        self.controlFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.controlFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.controlFrame.setObjectName(_fromUtf8("controlFrame"))
        self.controlWidget = QtGui.QWidget(self.controlFrame)
        self.controlWidget.setGeometry(QtCore.QRect(110, 0, 561, 61))
        self.controlWidget.setObjectName(_fromUtf8("controlWidget"))
        self.labelT = QtGui.QLabel(self.controlWidget)
        self.labelT.setGeometry(QtCore.QRect(0, 20, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelT.setFont(font)
        self.labelT.setObjectName(_fromUtf8("labelT"))
        self.textSliderValue = QtGui.QLabel(self.controlWidget)
        self.textSliderValue.setGeometry(QtCore.QRect(40, 20, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.textSliderValue.setFont(font)
        self.textSliderValue.setObjectName(_fromUtf8("textSliderValue"))
        self.slider = QtGui.QSlider(self.controlWidget)
        self.slider.setGeometry(QtCore.QRect(80, 10, 341, 41))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName(_fromUtf8("slider"))
        self.animationButton = QtGui.QPushButton(self.controlWidget)
        self.animationButton.setGeometry(QtCore.QRect(450, 10, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.animationButton.setFont(font)
        self.animationButton.setObjectName(_fromUtf8("animationButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1057, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHere = QtGui.QMenu(self.menubar)
        self.menuHere.setObjectName(_fromUtf8("menuHere"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuHere.addAction(self.actionExit)
        self.menubar.addAction(self.menuHere.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.labelT.setText(_translate("MainWindow", "T :", None))
        self.textSliderValue.setText(_translate("MainWindow", "0", None))
        self.animationButton.setText(_translate("MainWindow", "Animation", None))
        self.menuHere.setTitle(_translate("MainWindow", "File", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

