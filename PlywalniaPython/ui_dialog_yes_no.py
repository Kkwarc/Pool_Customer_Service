from PyQt5.QtCore import QCoreApplication, QMetaObject, Qt
from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QPushButton, QDialogButtonBox


class Ui_Dialog_Yes_No(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(200, 100)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.View = QTextEdit(Dialog)
        self.View.setObjectName(u"View")
        self.View.setReadOnly(True)

        self.verticalLayout.addWidget(self.View)

        self.addYesButton = QPushButton(Dialog)
        self.addYesButton.setObjectName(u"addYesButton")

        self.verticalLayout.addWidget(self.addYesButton)

        self.addNoButton = QPushButton(Dialog)
        self.addNoButton.setObjectName(u"addNoButton")

        self.verticalLayout.addWidget(self.addNoButton)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Data", None))
        self.addYesButton.setText(QCoreApplication.translate("Dialog", u"Yes", None))
        self.addNoButton.setText(QCoreApplication.translate("Dialog", u"No", None))
