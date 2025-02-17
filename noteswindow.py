# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NotesWidget(object):
    def setupUi(self, NotesWidget):
        NotesWidget.setObjectName("NotesWidget")
        NotesWidget.setMinimumSize(264, 279)
        NotesWidget.setAutoFillBackground(True)
        self.centralWidget = QtWidgets.QWidget(NotesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem)
        self.menuButton = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.menuButton.setFont(font)
        self.menuButton.setStyleSheet("QPushButton {\n" "    border: 0px;\n" "}")
        self.menuButton.setObjectName("moreButton")
        self.menuButton.setFixedSize(30, 30)  # Setting fixed size for more button
        self.horizontalLayout.addWidget(self.menuButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textEdit.setFont(font)
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setLineWidth(0)
        bg_color = self.centralWidget.palette().color(QtGui.QPalette.Window).name()
        self.textEdit.setStyleSheet(f"background-color: {bg_color}; border: none;")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        # Set layout to NotesWidget to apply the resizing behavior
        NotesWidget.setLayout(self.verticalLayout_2)

        # Set the size policy for resizable widgets
        self.textEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.menuButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.retranslateUi(NotesWidget)
        QtCore.QMetaObject.connectSlotsByName(NotesWidget)
        NotesWidget.adjustSize()

    def retranslateUi(self, NotesWidget):
        _translate = QtCore.QCoreApplication.translate
        NotesWidget.setWindowTitle(_translate("NotesWidget", "Failamp"))
