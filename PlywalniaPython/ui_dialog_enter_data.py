from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt
from PyQt5.QtWidgets import QVBoxLayout, QTextEdit, QPushButton, QDialogButtonBox, QFormLayout, QLabel, QCalendarWidget


class Ui_Dialog_Enter_Data(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.View = QTextEdit(Dialog)
        self.View.setObjectName(u"View")
        self.View.setReadOnly(True)

        self.verticalLayout.addWidget(self.View)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.date = QCalendarWidget(Dialog)
        self.date.setObjectName(u"Data")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.date)

        self.verticalLayout.addLayout(self.formLayout)

        self.addButton = QPushButton(Dialog)
        self.addButton.setObjectName(u"addButton")

        self.verticalLayout.addWidget(self.addButton)

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
        self.label.setText(QCoreApplication.translate("Dialog", u"Data", None))
        self.addButton.setText(QCoreApplication.translate("Dialog", u"Accept", None))
