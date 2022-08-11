# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListView, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        self.actionCredit = QAction(MainWindow)
        self.actionCredit.setObjectName(u"actionCredit")
        self.actionTHB_Wiki = QAction(MainWindow)
        self.actionTHB_Wiki.setObjectName(u"actionTHB_Wiki")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionJson_template = QAction(MainWindow)
        self.actionJson_template.setObjectName(u"actionJson_template")
        self.actionSave_2 = QAction(MainWindow)
        self.actionSave_2.setObjectName(u"actionSave_2")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.fileGroup = QGroupBox(self.centralwidget)
        self.fileGroup.setObjectName(u"fileGroup")
        self.fileGroup.setEnabled(True)
        self.fileGroup.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout_4 = QVBoxLayout(self.fileGroup)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.fileSelectText = QLineEdit(self.fileGroup)
        self.fileSelectText.setObjectName(u"fileSelectText")
        self.fileSelectText.setMinimumSize(QSize(0, 32))
        self.fileSelectText.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout_3.addWidget(self.fileSelectText)

        self.fileSelectButton = QPushButton(self.fileGroup)
        self.fileSelectButton.setObjectName(u"fileSelectButton")
        self.fileSelectButton.setMinimumSize(QSize(84, 32))
        self.fileSelectButton.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout_3.addWidget(self.fileSelectButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.fileListView = QListView(self.fileGroup)
        self.fileListView.setObjectName(u"fileListView")
        self.fileListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.fileListView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.fileListView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.horizontalLayout_4.addWidget(self.fileListView)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.fileClearButton = QPushButton(self.fileGroup)
        self.fileClearButton.setObjectName(u"fileClearButton")
        self.fileClearButton.setMinimumSize(QSize(84, 32))

        self.verticalLayout_3.addWidget(self.fileClearButton)

        self.fileReloadButton = QPushButton(self.fileGroup)
        self.fileReloadButton.setObjectName(u"fileReloadButton")
        self.fileReloadButton.setMinimumSize(QSize(84, 32))

        self.verticalLayout_3.addWidget(self.fileReloadButton)

        self.fileUpButton = QPushButton(self.fileGroup)
        self.fileUpButton.setObjectName(u"fileUpButton")
        self.fileUpButton.setMinimumSize(QSize(84, 32))

        self.verticalLayout_3.addWidget(self.fileUpButton)

        self.fileDownButton = QPushButton(self.fileGroup)
        self.fileDownButton.setObjectName(u"fileDownButton")
        self.fileDownButton.setMinimumSize(QSize(84, 32))

        self.verticalLayout_3.addWidget(self.fileDownButton)

        self.fileDeleteButton = QPushButton(self.fileGroup)
        self.fileDeleteButton.setObjectName(u"fileDeleteButton")
        self.fileDeleteButton.setMinimumSize(QSize(84, 32))

        self.verticalLayout_3.addWidget(self.fileDeleteButton)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.gridLayout.addWidget(self.fileGroup, 0, 0, 1, 1)

        self.editGroup = QGroupBox(self.centralwidget)
        self.editGroup.setObjectName(u"editGroup")
        self.editGroup.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout = QVBoxLayout(self.editGroup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.infoSourceCombo = QComboBox(self.editGroup)
        self.infoSourceCombo.setObjectName(u"infoSourceCombo")
        self.infoSourceCombo.setMinimumSize(QSize(84, 32))
        self.infoSourceCombo.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout.addWidget(self.infoSourceCombo)

        self.infoSearchKeyText = QLineEdit(self.editGroup)
        self.infoSearchKeyText.setObjectName(u"infoSearchKeyText")
        self.infoSearchKeyText.setMinimumSize(QSize(0, 32))
        self.infoSearchKeyText.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout.addWidget(self.infoSearchKeyText)

        self.infoSearchButton = QPushButton(self.editGroup)
        self.infoSearchButton.setObjectName(u"infoSearchButton")
        self.infoSearchButton.setMinimumSize(QSize(84, 32))
        self.infoSearchButton.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout.addWidget(self.infoSearchButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fileRenameText = QLineEdit(self.editGroup)
        self.fileRenameText.setObjectName(u"fileRenameText")
        self.fileRenameText.setEnabled(False)
        self.fileRenameText.setMinimumSize(QSize(0, 32))
        self.fileRenameText.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout_2.addWidget(self.fileRenameText)

        self.fileRenameCheck = QCheckBox(self.editGroup)
        self.fileRenameCheck.setObjectName(u"fileRenameCheck")
        self.fileRenameCheck.setMinimumSize(QSize(84, 32))
        self.fileRenameCheck.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout_2.addWidget(self.fileRenameCheck)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.albumCoverLable = QLabel(self.editGroup)
        self.albumCoverLable.setObjectName(u"albumCoverLable")
        self.albumCoverLable.setMinimumSize(QSize(128, 0))
        self.albumCoverLable.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_2.addWidget(self.albumCoverLable, 1, 1, 1, 1)

        self.albumCover = QLabel(self.editGroup)
        self.albumCover.setObjectName(u"albumCover")
        self.albumCover.setMinimumSize(QSize(100, 100))
        self.albumCover.setMaximumSize(QSize(16777215, 16777215))
        self.albumCover.setTextFormat(Qt.AutoText)
        self.albumCover.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.albumCover, 0, 1, 1, 1)

        self.infoTableView = QTableView(self.editGroup)
        self.infoTableView.setObjectName(u"infoTableView")

        self.gridLayout_2.addWidget(self.infoTableView, 0, 0, 2, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.gridLayout.addWidget(self.editGroup, 1, 0, 1, 1)

        self.tagGroup = QGroupBox(self.centralwidget)
        self.tagGroup.setObjectName(u"tagGroup")
        self.tagGroup.setSizeIncrement(QSize(0, 0))
        self.tagGroup.setBaseSize(QSize(0, 0))
        self.tagGroup.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout_2 = QVBoxLayout(self.tagGroup)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tagTableView = QTableView(self.tagGroup)
        self.tagTableView.setObjectName(u"tagTableView")
        self.tagTableView.setMinimumSize(QSize(350, 0))
        self.tagTableView.setSizeIncrement(QSize(0, 0))

        self.verticalLayout_2.addWidget(self.tagTableView)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(50)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(50, -1, 50, -1)
        self.tagImportButton = QPushButton(self.tagGroup)
        self.tagImportButton.setObjectName(u"tagImportButton")
        self.tagImportButton.setMinimumSize(QSize(84, 32))
        self.tagImportButton.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout_5.addWidget(self.tagImportButton)

        self.tagSaveButton = QPushButton(self.tagGroup)
        self.tagSaveButton.setObjectName(u"tagSaveButton")
        self.tagSaveButton.setMinimumSize(QSize(84, 32))
        self.tagSaveButton.setMaximumSize(QSize(16777215, 32))
        self.tagSaveButton.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_5.addWidget(self.tagSaveButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.gridLayout.addWidget(self.tagGroup, 0, 1, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 30))
        self.menuSource = QMenu(self.menubar)
        self.menuSource.setObjectName(u"menuSource")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSource.menuAction())
        self.menuSource.addAction(self.actionCredit)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionJson_template)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_2)
        self.menuFile.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"thtagger - weilinfox", None))
        self.actionCredit.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionTHB_Wiki.setText(QCoreApplication.translate("MainWindow", u"THB Wiki", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Open folder(s)", None))
        self.actionJson_template.setText(QCoreApplication.translate("MainWindow", u"Json template", None))
        self.actionSave_2.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.fileGroup.setTitle(QCoreApplication.translate("MainWindow", u"Open folder(s)", None))
        self.fileSelectButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.fileClearButton.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.fileReloadButton.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.fileUpButton.setText(QCoreApplication.translate("MainWindow", u"Up", None))
        self.fileDownButton.setText(QCoreApplication.translate("MainWindow", u"Down", None))
        self.fileDeleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.editGroup.setTitle(QCoreApplication.translate("MainWindow", u"Track information", None))
        self.infoSearchButton.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.fileRenameCheck.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.albumCoverLable.setText("")
        self.albumCover.setText(QCoreApplication.translate("MainWindow", u"No image", None))
        self.tagGroup.setTitle(QCoreApplication.translate("MainWindow", u"Tag information", None))
        self.tagImportButton.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.tagSaveButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.menuSource.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

