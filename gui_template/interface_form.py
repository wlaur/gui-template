# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_template\ui\interface.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(800, 600)
        TabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        TabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        TabWidget.setIconSize(QtCore.QSize(30, 30))
        TabWidget.setUsesScrollButtons(False)
        TabWidget.setDocumentMode(False)
        TabWidget.setTabsClosable(False)
        self.MainTab = QtWidgets.QWidget()
        self.MainTab.setObjectName("MainTab")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.MainTab)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.TestButton = QtWidgets.QPushButton(self.MainTab)
        self.TestButton.setObjectName("TestButton")
        self.gridLayout_8.addWidget(self.TestButton, 4, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem1, 0, 1, 1, 1)
        self.ShowProgressButton = QtWidgets.QPushButton(self.MainTab)
        self.ShowProgressButton.setObjectName("ShowProgressButton")
        self.gridLayout_8.addWidget(self.ShowProgressButton, 3, 1, 1, 1)
        self.FilesSelectButton = QtWidgets.QPushButton(self.MainTab)
        self.FilesSelectButton.setObjectName("FilesSelectButton")
        self.gridLayout_8.addWidget(self.FilesSelectButton, 2, 1, 1, 1)
        self.FolderSelectButton = QtWidgets.QPushButton(self.MainTab)
        self.FolderSelectButton.setObjectName("FolderSelectButton")
        self.gridLayout_8.addWidget(self.FolderSelectButton, 1, 1, 1, 1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui_template\\ui\\../../assets/load-icon-inverted.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TabWidget.addTab(self.MainTab, icon, "")
        self.SettingsTab = QtWidgets.QWidget()
        self.SettingsTab.setObjectName("SettingsTab")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.SettingsTab)
        self.gridLayout_15.setObjectName("gridLayout_15")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("gui_template\\ui\\../../assets/settings-icon-inverted.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TabWidget.addTab(self.SettingsTab, icon1, "")
        self.ToolsTab = QtWidgets.QWidget()
        self.ToolsTab.setObjectName("ToolsTab")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.ToolsTab)
        self.gridLayout_14.setObjectName("gridLayout_14")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("gui_template\\ui\\../../assets/tools-icon-inverted.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TabWidget.addTab(self.ToolsTab, icon2, "")
        self.LogTab = QtWidgets.QWidget()
        self.LogTab.setObjectName("LogTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.LogTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.LogBrowser = QtWidgets.QTextBrowser(self.LogTab)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.LogBrowser.setFont(font)
        self.LogBrowser.setFrameShadow(QtWidgets.QFrame.Plain)
        self.LogBrowser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.LogBrowser.setObjectName("LogBrowser")
        self.gridLayout_3.addWidget(self.LogBrowser, 0, 0, 1, 1)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("gui_template\\ui\\../../assets/log-icon-inverted.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TabWidget.addTab(self.LogTab, icon3, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.TestButton.setText(_translate("TabWidget", "Button"))
        self.ShowProgressButton.setText(_translate("TabWidget", "Progress"))
        self.FilesSelectButton.setText(_translate("TabWidget", "Files"))
        self.FolderSelectButton.setText(_translate("TabWidget", "Folder"))
        TabWidget.setTabText(TabWidget.indexOf(self.MainTab), _translate("TabWidget", "Main"))
        TabWidget.setTabText(TabWidget.indexOf(self.SettingsTab), _translate("TabWidget", "Settings"))
        TabWidget.setTabText(TabWidget.indexOf(self.ToolsTab), _translate("TabWidget", "Tools"))
        TabWidget.setTabText(TabWidget.indexOf(self.LogTab), _translate("TabWidget", "Log"))
