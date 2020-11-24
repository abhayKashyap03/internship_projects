# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, data):
        self.data = data
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1044, 730)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QtCore.QRect(185, 100, 341, 61))
        self.textEdit.setObjectName("textEdit")
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(-4, 0, 1051, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_0.setFont(font)
        self.label_0.setAlignment(QtCore.Qt.AlignCenter)
        self.label_0.setObjectName("label_0")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 100, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 200, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(25, 290, 140, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 450, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(620, 100, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(600, 170, 341, 241))
        self.label_6.setObjectName("label_6")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(185, 190, 341, 61))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(185, 300, 341, 121))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(185, 460, 341, 111))
        self.textEdit_4.setObjectName("textEdit_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(420, 620, 89, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(310, 620, 89, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(200, 620, 89, 25))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(718, 450, 101, 25))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1044, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.pushButton.clicked.connect(lambda : self.get_image())
        self.pushButton_3.clicked.connect(lambda : self.exit_button())
        self.pushButton_4.clicked.connect(lambda : self.clear_text())
        self.pushButton_5.clicked.connect(lambda : self.save_data())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_0.setText(_translate("MainWindow", "Human Assets Information Records"))
        self.label.setText(_translate("MainWindow", "NAME"))
        self.label_2.setText(_translate("MainWindow", "ID"))
        self.label_3.setText(_translate("MainWindow", "DESCRIPTION"))
        self.label_4.setText(_translate("MainWindow", "NOTES"))
        self.label_5.setText(_translate("MainWindow", "PICTURES"))
        self.pushButton_3.setText(_translate("MainWindow", "Exit"))
        self.pushButton_4.setText(_translate("MainWindow", "Reset"))
        self.pushButton_5.setText(_translate("MainWindow", "Save"))
        self.pushButton.setText(_translate("MainWindow", "Insert Image"))

    def get_image(self) :
        self.data_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', r"/home/abhay_kashyap03/", "Images (*.png *.xpm *.jpg, *.bpm, *.jpeg)")
        pixmap = QtGui.QPixmap(self.data_path)
        self.label_6.setPixmap(pixmap.scaled(self.label_6.size(), QtCore.Qt.IgnoreAspectRatio))

    def exit_button(self) :
        sys.exit()

    def clear_text(self) :
        self.textEdit.setText("")
        self.textEdit_2.setText("")
        self.textEdit_3.setText("")
        self.textEdit_4.setText("")
        self.label_6.clear()

    def save_data(self) :
        name = self.textEdit.toPlainText()
        id = self.textEdit_2.toPlainText()
        desc = self.textEdit_3.toPlainText()
        notes = self.textEdit_4.toPlainText()
        try :
            new_data = {"Name" : name, "ID" : id, "Description" : desc, "Notes" : notes, "Image Path" : self.data_path}
        except Exception :
            new_data = {"Name" : name, "ID" : id, "Description" : desc, "Notes" : notes, "Image Path" : "No image"}
        self.data = self.data.append(new_data, ignore_index=True)
        self.data.to_csv("/home/abhay_kashyap03/Desktop/test.csv", index=False)
        

if __name__ == "__main__":
    import sys, os, pandas as pd
    if os.path.exists("/home/abhay_kashyap03/Desktop/test.csv") :
        data = pd.read_csv("/home/abhay_kashyap03/Desktop/test.csv")
    else :
        data = pd.DataFrame(columns=["Name", "ID", "Description", "Notes", "Image Path"])
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, data)
    MainWindow.show()
    sys.exit(app.exec_())

