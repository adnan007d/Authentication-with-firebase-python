import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import pyrebase

firebaseConfig = {
    #Add your firebase config here
  }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('login.ui',self)
        self.initUi()
    
    def initUi(self):
        self.Email_Error.setVisible(False)
        self.Password_Error.setVisible(False)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Login.clicked.connect(self.Creds)
        self.Signup.clicked.connect(self.GotoSignup)
        self.Forgot_Pass.clicked.connect(self.Reset_Password)
    def Creds(self):
        Email = str(self.Email.text()).strip()
        Passwd = str(self.Password.text())
        self.Label_Error.setStyleSheet('color:red;')
        if Email == '' or Passwd == '':
            self.Email_Error.setVisible(True)
            self.Password_Error.setVisible(True)
            self.Label_Error.setText('*Email and Password Cannot be empty')
        elif len(Passwd) < 8:
            self.Password_Error.setVisible(True)
            self.Email_Error.setVisible(False)
            self.Label_Error.setText("*Password should be at least 8 characters")
        else:
            self.Email_Error.setVisible(False)
            self.Password_Error.setVisible(False)
            self.Label_Error.setText('')
            try:
                user = auth.sign_in_with_email_and_password(Email,Passwd)
                info = auth.get_account_info(user['idToken'])['users'][0]['email']
                verified = auth.get_account_info(user['idToken'])['users'][0]['emailVerified']
                if verified:
                    Main = Home(info)
                    widget.addWidget(Main)
                    widget.setWindowTitle('Home')
                    widget.setFixedWidth(663)
                    widget.setFixedHeight(553)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                else:
                    self.Label_Error.setText("Please verify your email")
            except Exception as e:
                err = e.args[1]
                err = err.split('\n')[3].strip()[:-1][12:-1]
                if err == "INVALID_EMAIL":
                    self.Email_Error.setVisible(True)
                    self.Label_Error.setText("*Enter a Valid Email")
                elif err in ["EMAIL_NOT_FOUND","INVALID_PASSWORD"]:
                    self.Email_Error.setVisible(True)
                    self.Password_Error.setVisible(True)
                    self.Label_Error.setText("*Incorrect Email or Password")
                else:
                    self.Email_Error.setVisible(False)
                    self.Password_Error.setVisible(False)
                    self.Label_Error.setText("*Something went wrong")
    def GotoSignup(self):
        self.Email.setText('')
        self.Password.setText('')
        Sign = SignUp()
        widget.addWidget(Sign)
        widget.setWindowTitle('Sign Up')
        widget.setFixedWidth(364)
        widget.setFixedHeight(552)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def Reset_Password(self):
        reset = Reset()
        widget.addWidget(reset)
        widget.setWindowTitle('Password Reset')
        widget.setFixedWidth(361)
        widget.setFixedHeight(360)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SignUp(QMainWindow):
    def __init__(self):
        super(SignUp,self).__init__()
        loadUi('sigup.ui',self)
        self.initUi()

    def initUi(self):
        self.Email_Error.setVisible(False)
        self.Password_Error.setVisible(False)
        self.Confirm_Password_Error.setVisible(False)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Confirm_Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.SignUp.clicked.connect(self.Creds)
        self.Login.clicked.connect(self.GotoLogin)
        
    
    def Creds(self):
        Email = str(self.Email.text()).strip()
        Passwd = str(self.Password.text())
        Conf_Passwd = str(self.Confirm_Password.text())
        self.Label_Error.setStyleSheet('color:red;')
        if Passwd != Conf_Passwd:
            self.Password_Error.setVisible(True)
            self.Confirm_Password_Error.setVisible(True)
            self.Label_Error.setText('*Both Passwords should be same')
        elif Email == '' or Passwd == '':
            self.Email_Error.setVisible(True)
            self.Password_Error.setVisible(True)
            self.Confirm_Password_Error.setVisible(True)
            self.Label_Error.setText('*Email and Password Cannot be empty')
        elif len(Passwd) < 8:
            self.Password_Error.setVisible(True)
            self.Confirm_Password_Error.setVisible(True)
            self.Label_Error.setText('*Password should at least be 8 characters')
        else:
            try:
                user = auth.create_user_with_email_and_password(Email,Passwd)
                self.Email.setText('')
                self.Password.setText('')
                self.Confirm_Password.setText('')
                self.Email_Error.setVisible(False)
                self.Password_Error.setVisible(False)
                self.Confirm_Password_Error.setVisible(False)
                self.Label_Error.setText("")
                auth.send_email_verification(user['idToken'])
                login = Login()
                login.Label_Error.setStyleSheet('color:green;')
                login.Label_Error.setText("Verify your Email")
                widget.addWidget(login)
                widget.setWindowTitle('Login')
                widget.setFixedWidth(364)
                widget.setFixedHeight(552)
                widget.setCurrentIndex(widget.currentIndex()+1)
            except Exception as e:
                err = e.args[1]
                err = err.split('\n')[3].strip()[:-1][12:-1]
                if err == "INVALID_EMAIL":
                    self.Email_Error.setVisible(True)
                    self.Label_Error.setText('*Enter a valid Email')
                elif err == "EMAIL_EXISTS":
                    self.Email_Error.setVisible(True)
                    self.Label_Error.setText('*Email already exists')
                else:
                    self.Email_Error.setVisible(False)
                    self.Password_Error.setVisible(False)
                    self.Confirm_Password_Error.setVisible(False)
                    self.Label_Error.setText("*Something went wrong")
    def GotoLogin(self):
        self.Email.setText('')
        self.Password.setText('')
        self.Confirm_Password.setText('')
        login = Login()
        widget.addWidget(login)
        widget.setWindowTitle('Login')
        widget.setFixedWidth(364)
        widget.setFixedHeight(552)
        widget.setCurrentIndex(widget.currentIndex()+1)

    
class Home(QMainWindow):
    def __init__(self,info):
        super(Home,self).__init__()
        loadUi('Main.ui',self)
        self.info = info
        self.initUi()
    def initUi(self):
        self.Name.setText(self.info)
        self.Button1.clicked.connect(self.Image1)
        self.Button2.clicked.connect(self.Image2)
        self.Logout.clicked.connect(self.lOut)
    def Image1(self):
        self.Image.setPixmap(QPixmap('image/1.jpg'))

    def Image2(self):
        self.Image.setPixmap(QPixmap('image/2.jpg'))

    def lOut(self):
        login = Login()
        widget.addWidget(login)
        widget.setWindowTitle('Login')
        widget.setFixedWidth(364)
        widget.setFixedHeight(552)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Reset(QMainWindow):
    def __init__(self):
        super(Reset,self).__init__()
        loadUi('Forgot.ui',self)
        self.initUi()

    def initUi(self):
        self.Email_Error.setVisible(False)
        self.Reset.clicked.connect(self.sendMail)
        self.Login.clicked.connect(self.GotoLogin)
        
    def sendMail(self):
        self.Email_Error.setVisible(False)
        self.Label_Error.setStyleSheet('color:red;')
        Email = str(self.Email.text()).strip()
        if Email == '':
            self.Label_Error.setText("*Email cannot be empty")
            self.Email_Error.setVisible(True)
        else:
            self.Email_Error.setVisible(False)
            try:
                auth.send_password_reset_email(Email)
                self.Label_Error.setStyleSheet('color:green;')
                self.Label_Error.setText("Check your mail for password reset")
            except Exception as e:
                err = e.args[1].split('\n')[3].strip()[:-1][12:-1]
                if err == 'INVALID_EMAIL':
                    self.Email_Error.setVisible(True)
                    self.Label_Error.setText("*Invalid Email")
                elif err == 'EMAIL_NOT_FOUND':
                    self.Email_Error.setVisible(True)
                    self.Label_Error.setText("*Email not found")
                else:
                    self.Label_Error.setText("*Something Went Wrong")


    def GotoLogin(self):
        login = Login()
        widget.addWidget(login)
        widget.setWindowTitle('Login')
        widget.setFixedWidth(364)
        widget.setFixedHeight(552)
        widget.setCurrentIndex(widget.currentIndex()+1)
                
app = QApplication(sys.argv)
win = Login()
widget = QtWidgets.QStackedWidget()
win.setFixedWidth(364)
win.setFixedHeight(552)
win.setWindowTitle('Login')
widget.addWidget(win)
widget.setWindowTitle('Login')
widget.move(500,100)
widget.show()

sys.exit(app.exec_())