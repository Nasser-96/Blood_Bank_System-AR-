from PyQt5.QtWidgets import *

import MySQLdb
import sys
from os import path
from PyQt5.uic import loadUiType

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "Donor_window.ui"))
FORM_CLASS2, _ = loadUiType(path.join(path.dirname(__file__), "login.ui"))
FORM_CLASS3, _ = loadUiType(path.join(path.dirname(__file__), "Acceptor_window.ui"))


class login(QMainWindow, FORM_CLASS2):
    def __init__(self, parent=None):
        super(login, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_DB_Connection()
        self.window2 = None
        self.Handel_buttons_login()



    def handel_login(self):
        try:
            username = self.lineEdit.text()
            password = self.lineEdit_2.text()
            sql = '''SELECT * FROM users'''
            self.cur.execute(sql)
            data = self.cur.fetchall()
            for row in data:
                if row[1] == username and row[2] == password and row[3] == 'donor':
                    self.username2 = username
                    self.window2 = Main(self.username2)
                    self.close()
                    self.window2.show()
                elif row[1] == username and row[2] == password and row[3] == 'acceptor':
                    self.username2 = username
                    self.window3 = acceptor(self.username2)
                    self.close()
                    self.window3.show()

                else:
                    self.label_5.setText('اسم المستخدم او كلمة المرور خاطئة')
        except Exception as e:
            print(e)

    def Handle_DB_Connection(self):
        ## Database connection
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="blood_bank")
        self.cur = self.db.cursor()
        print('connection Done')

    def Handel_buttons_login(self):
        self.pushButton_2.clicked.connect(self.Create_User)
        self.pushButton.clicked.connect(self.handel_login)

    def Create_User(self):
        print('You are in Create user')

        email = self.lineEdit_3.text()
        password1 = self.lineEdit_4.text()
        password2 = self.lineEdit_5.text()
        type_1 = "donor"
        type_2 = "acceptor"
        sql = '''SELECT * FROM users'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        try:
            for row in data:
                if self.radioButton.isChecked() == True:
                    if row[1] == email:
                        self.label.setText('اسم المستخدم موجود مسبقا')
                    if password1 == password2 and len(password1) >= 8:
                        self.cur.execute('''INSERT INTO users(email ,pass,user_type) VALUES(%s,%s,%s)''',
                                         (email, password1, type_1))
                        self.cur.execute('''INSERT INTO donor_info(email ) VALUES(%s)''', (email,))
                        self.db.commit()
                        self.statusbar.showMessage('تم اضافة المستخدم بنجاح')
                    elif len(password1) < 8:
                        self.label_2.setText('كلمة السر يجب ان تكون اكثر من 8 خانات')
                    elif password1 != password2:
                        self.label_4.setText('كلمة السر غير مطابقة')
                elif self.radioButton_2.isChecked() == True:
                    if row[1] == email:
                        self.label.setText('اسم المستخدم موجود مسبقا')
                    if password1 == password2 and len(password1) >= 8:
                        self.cur.execute('''INSERT INTO users(email ,pass,user_type) VALUES(%s,%s,%s)''',
                                         (email, password1, type_2))
                        self.cur.execute('''INSERT INTO acceptor_info(email) VALUES(%s)''', (email,))
                        self.db.commit()
                        self.statusbar.showMessage('تم اضافة المستخدم بنجاح')
                    elif len(password1) < 8:
                        self.label_2.setText('كلمة السر يجب ان تكون اكثر من 8 خانات')
                    elif password1 != password2:
                        self.label_4.setText('كلمة السر غير مطابقة')
                else:
                    self.label_3.setText('الرجاء ملء جميع الخانات')
        except Exception as e:
            print(e)


####################################################################
## second window

class Main(QMainWindow, FORM_CLASS):
    def __init__(self,username2, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handle_DB_Connection()
        self.Handel_buttons()
        username1 = username2
        self.lineEdit_17.setText(username1)


    def InitUI(self):
        ## changes in run time
        self.setWindowTitle('برنامج بنك الدم')
        self.lineEdit_17.setVisible(False)

    def Handle_DB_Connection(self):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="blood_bank")
        self.cur = self.db.cursor()

    def Handel_buttons(self):
        self.pushButton.clicked.connect(self.Update_Donor_Info)
        self.pushButton_2.clicked.connect(self.Update_Donor_Info)
        self.pushButton_3.clicked.connect(self.Take_Back_Info)
        self.pushButton_4.clicked.connect(self.Search)


    def Update_Donor_Info(self):
        card_id = self.lineEdit.text()
        first_name = self.lineEdit_2.text()
        last_name = self.lineEdit_3.text()
        age = self.lineEdit_4.text()
        gender = self.comboBox.currentIndex()
        blood_type = self.comboBox_2.currentIndex()
        Nationality = self.lineEdit_5.text()
        phone_number = self.lineEdit_6.text()
        address = self.lineEdit_7.text()
        purpose_of_donation = self.lineEdit_8.text()
        username = self.lineEdit_17.text()

        try:
            self.cur.execute(
                '''UPDATE donor_info SET card_id=%s,first_name=%s,last_name=%s ,age=%s ,gender=%s ,blood_type=%s ,nationality=%s ,
                phone_number=%s, address=%s ,purpose_of_donation=%s  WHERE email =%s ''',
                (card_id,first_name,last_name,age,gender,blood_type,Nationality,phone_number,address,purpose_of_donation,username ))
            self.db.commit()

            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.comboBox.setCurrentIndex(0)
            self.comboBox_2.setCurrentIndex(0)
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')
            self.lineEdit_8.setText('')

            self.statusbar.showMessage('تم اضافة المعلومات المعلومات بنجاح')
        except Exception as e:
            print(e)


    def Take_Back_Info(self):
        try:
            sql = '''SELECT * FROM donor_info WHERE email = %s'''
            email = self.lineEdit_17.text()
            self.cur.execute(sql, [(email)])
            data = self.cur.fetchall()
            for row in data:
                self.lineEdit.setText(str(row[1]))
                self.lineEdit_2.setText(str(row[2]))
                self.lineEdit_3.setText(str(row[3]))
                self.lineEdit_4.setText(str(row[4]))
                self.comboBox.setCurrentIndex(int(row[5]))
                self.comboBox_2.setCurrentIndex(int(row[6]))
                self.lineEdit_5.setText(str(row[7]))
                self.lineEdit_6.setText(str(row[8]))
                self.lineEdit_7.setText(str(row[9]))
                self.lineEdit_8.setText(str(row[10]))

        except Exception as e:
            print(e)


    def Search(self):

        try:
            self.tableWidget.insertRow(0)
            if self.radioButton.isChecked() == True:
                sql = '''SELECT first_name ,last_name,phone_number FROM donor_info WHERE blood_type = %s'''
                blood_type = self.comboBox_3.currentIndex()
                self.cur.execute(sql,[(blood_type)])
                for row, data in enumerate(self.cur):
                    for column, item in enumerate(data):
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)
        except Exception as e:
            print(e)


        try:
            self.tableWidget.insertRow(0)
            if self.radioButton_2.isChecked() == True:
                sql = '''SELECT first_name ,last_name,phone_number,number_of_blood_units FROM acceptor_info WHERE blood_type = %s'''
                blood_type = self.comboBox_3.currentIndex()
                self.cur.execute(sql,[(blood_type)])
                for row, data in enumerate(self.cur):
                    for column, item in enumerate(data):
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)
        except Exception as e:
            print(e)





    ###############################################################
    ##Acceptor Window

class acceptor(QMainWindow, FORM_CLASS3):
    def __init__(self,username2, parent=None):
        super(acceptor, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handle_DB_Connection()
        self.Handel_buttons()
        username1 = username2
        self.lineEdit_17.setText(username1)

    def InitUI(self):
        self.setWindowTitle('برنامج بنك الدم')
        self.lineEdit_17.setVisible(False)

    def Handle_DB_Connection(self):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="blood_bank")
        self.cur = self.db.cursor()

    def Handel_buttons(self):
        self.pushButton_3.clicked.connect(self.Update_Acceptor_Info)
        self.pushButton_4.clicked.connect(self.Update_Acceptor_Info)
        self.pushButton_5.clicked.connect(self.Take_Back_Info)
        self.pushButton_6.clicked.connect(self.Search)

    def Update_Acceptor_Info(self):
        card_id = self.lineEdit_9.text()
        first_name = self.lineEdit_10.text()
        last_name = self.lineEdit_11.text()
        age = self.lineEdit_12.text()
        gender = self.comboBox_3.currentIndex()
        blood_type = self.comboBox_4.currentIndex()
        Nationality = self.lineEdit_13.text()
        phone_number = self.lineEdit_14.text()
        address = self.lineEdit_15.text()
        number_of_blood_units = self.lineEdit_16.text()
        username = self.lineEdit_17.text()

        try:
            self.cur.execute(
                '''UPDATE acceptor_info SET card_id=%s,first_name=%s,last_name=%s ,age=%s ,gender=%s ,blood_type=%s ,nationality=%s ,
                phone_number=%s, address=%s ,number_of_blood_units=%s  WHERE email =%s ''',
                (card_id, first_name, last_name, age, gender, blood_type, Nationality, phone_number, address,
                 number_of_blood_units, username))
            self.db.commit()

            self.lineEdit_9.setText('')
            self.lineEdit_10.setText('')
            self.lineEdit_11.setText('')
            self.lineEdit_12.setText('')
            self.comboBox_3.setCurrentIndex(0)
            self.comboBox_4.setCurrentIndex(0)
            self.lineEdit_13.setText('')
            self.lineEdit_14.setText('')
            self.lineEdit_15.setText('')
            self.lineEdit_16.setText('')

            self.statusbar.showMessage('تم اضافة المعلومات المعلومات بنجاح')
        except Exception as e:
            print(e)

    def Take_Back_Info(self):
        try:
            sql = '''SELECT * FROM acceptor_info WHERE email = %s'''
            email = self.lineEdit_17.text()
            self.cur.execute(sql, [(email)])
            data = self.cur.fetchall()
            for row in data:
                self.lineEdit_9.setText(str(row[1]))
                self.lineEdit_10.setText(str(row[2]))
                self.lineEdit_11.setText(str(row[3]))
                self.lineEdit_12.setText(str(row[4]))
                self.comboBox_3.setCurrentIndex(int(row[5]))
                self.comboBox_4.setCurrentIndex(int(row[6]))
                self.lineEdit_13.setText(str(row[7]))
                self.lineEdit_14.setText(str(row[8]))
                self.lineEdit_15.setText(str(row[9]))
                self.lineEdit_16.setText(str(row[10]))

        except Exception as e:
            print(e)



    def Search(self):

        try:
            self.tableWidget.insertRow(0)
            if self.radioButton.isChecked() == True:
                sql = '''SELECT first_name ,last_name,phone_number FROM donor_info WHERE blood_type = %s'''
                blood_type = self.comboBox_5.currentIndex()
                self.cur.execute(sql,[(blood_type)])
                for row, data in enumerate(self.cur):
                    for column, item in enumerate(data):
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)
        except Exception as e:
            print(e)


        try:
            self.tableWidget.insertRow(0)
            if self.radioButton_2.isChecked() == True:
                sql = '''SELECT first_name ,last_name,phone_number,number_of_blood_units FROM acceptor_info WHERE blood_type = %s'''
                blood_type = self.comboBox_5.currentIndex()
                self.cur.execute(sql,[(blood_type)])
                for row, data in enumerate(self.cur):
                    for column, item in enumerate(data):
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)
        except Exception as e:
            print(e)



def main():
    app = QApplication(sys.argv)
    # window = Main()
    window = login()
    window.show()
    app.exec_()  ## App Main Loop


if __name__ == '__main__':  ## Statr Run From Here
    main()
