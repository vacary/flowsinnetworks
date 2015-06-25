# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface7.ui'
#
# Created: Tue Jun 23 22:56:03 2015
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
        MainWindow.resize(1079, 754)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_5 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.controlFrame_4 = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlFrame_4.sizePolicy().hasHeightForWidth())
        self.controlFrame_4.setSizePolicy(sizePolicy)
        self.controlFrame_4.setMinimumSize(QtCore.QSize(0, 40))
        self.controlFrame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.controlFrame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.controlFrame_4.setObjectName(_fromUtf8("controlFrame_4"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.controlFrame_4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_2 = QtGui.QWidget(self.controlFrame_4)
        self.widget_2.setMinimumSize(QtCore.QSize(20, 0))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout.addWidget(self.widget_2)
        self.labelT_11 = QtGui.QLabel(self.controlFrame_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelT_11.setFont(font)
        self.labelT_11.setObjectName(_fromUtf8("labelT_11"))
        self.horizontalLayout.addWidget(self.labelT_11)
        self.textSliderValue_11 = QtGui.QLabel(self.controlFrame_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.textSliderValue_11.setFont(font)
        self.textSliderValue_11.setObjectName(_fromUtf8("textSliderValue_11"))
        self.horizontalLayout.addWidget(self.textSliderValue_11)
        self.widget = QtGui.QWidget(self.controlFrame_4)
        self.widget.setMinimumSize(QtCore.QSize(25, 0))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout.addWidget(self.widget)
        self.slider_11 = QtGui.QSlider(self.controlFrame_4)
        self.slider_11.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider_11.setOrientation(QtCore.Qt.Horizontal)
        self.slider_11.setObjectName(_fromUtf8("slider_11"))
        self.horizontalLayout.addWidget(self.slider_11)
        self.widget_3 = QtGui.QWidget(self.controlFrame_4)
        self.widget_3.setMinimumSize(QtCore.QSize(30, 0))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout.addWidget(self.widget_3)
        self.animationButton_11 = QtGui.QPushButton(self.controlFrame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.animationButton_11.sizePolicy().hasHeightForWidth())
        self.animationButton_11.setSizePolicy(sizePolicy)
        self.animationButton_11.setMinimumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.animationButton_11.setFont(font)
        self.animationButton_11.setObjectName(_fromUtf8("animationButton_11"))
        self.horizontalLayout.addWidget(self.animationButton_11)
        self.widget_4 = QtGui.QWidget(self.controlFrame_4)
        self.widget_4.setMinimumSize(QtCore.QSize(30, 0))
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.horizontalLayout.addWidget(self.widget_4)
        self.gridLayout_5.addWidget(self.controlFrame_4, 1, 0, 1, 1)
        self.vtkFrame_4 = QtGui.QFrame(self.centralwidget)
        self.vtkFrame_4.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vtkFrame_4.sizePolicy().hasHeightForWidth())
        self.vtkFrame_4.setSizePolicy(sizePolicy)
        self.vtkFrame_4.setAutoFillBackground(False)
        self.vtkFrame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.vtkFrame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.vtkFrame_4.setObjectName(_fromUtf8("vtkFrame_4"))
        self.gridLayout_5.addWidget(self.vtkFrame_4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1079, 25))
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
        self.labelT_11.setText(_translate("MainWindow", "T :", None))
        self.textSliderValue_11.setText(_translate("MainWindow", "0", None))
        self.animationButton_11.setText(_translate("MainWindow", "Play", None))
        self.menuHere.setTitle(_translate("MainWindow", "File", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

