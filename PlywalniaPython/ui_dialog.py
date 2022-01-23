from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QTextEdit, QLabel, QCalendarWidget, QSpinBox, QPushButton, QDialogButtonBox, QLineEdit

import datetime


class Ui_Dialog(object):
    date_today = datetime.date.today()
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")

        self.View = QTextEdit(Dialog)
        self.View.setObjectName(u"View")
        self.View.setReadOnly(True)

        self.verticalLayout.addWidget(self.View)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.name = QLineEdit(Dialog)
        self.name.setObjectName(u"Name")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.name)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.date = QCalendarWidget(Dialog)
        self.date.setMinimumDate(self.date_today)
        self.date.setObjectName(u"Data")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.date)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.hour = QSpinBox(Dialog)
        self.hour.setObjectName(u"Hour")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.hour)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.number = QSpinBox(Dialog)
        self.number.setMinimum(1)
        self.number.setObjectName(u"Number of tracks/seats")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.number)

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
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New Reservation", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Date", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Hour", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Number", None))
        self.addButton.setText(QCoreApplication.translate("Dialog", u"Accept", None))
