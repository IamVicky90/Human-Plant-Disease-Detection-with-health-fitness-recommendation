import smtplib
from datetime import datetime
import os
from src.loggings import add_logger
from threading import Thread
class mail():
    def __init__(self)->None:
        self.log=add_logger()
    def send_mail(self,email,message)->None:
        '''
        To send email to specific email address
        params: 
            email: email address of the reciever.
            message: Message to send the reciever.
        '''
        # .................Old Method..................
        # port = 465  # For SSL
        # smtp_server = "smtp.gmail.com"
        # sender_email = "vickyaiproduction@gmail.com"  # Enter your address
        # receiver_email = email  # Enter receiver address
        # password = os.environ.get('MAIL_PASSWORD')
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        #     server.login(sender_email, password)
        #     server.sendmail(sender_email, receiver_email, message)
        # .................Old Method.................
        
        send_mail_with_threading(email,message).start()
       
    def user_login_mail(self,email):
        '''Take the email address to send mail
        args: 
            email: email address of a user.'''
        dt=datetime.now()
        message = f"""\
    Subject: Log-in Alert

    Dear User:\n\t\tYou have successfully logged on to Human and Plant Disease Detection with Health and Physical fitness recommendation App dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]} hours.\n\nRegards: Vicky AI Production"""
        self.send_mail(email=email,message=message)
        self.log.log(f'Login mail send to email: {str(email)}','emails.log',1)
    def user_signup_confirmation_mail(self,email):
        '''Take the email address to send mail
        args: 
            email: email address of a user.'''
        dt=datetime.now()
        message = f"""\
    Subject: Sign-Up Sucessfully

    Dear User:\n\t\tYou have successfully Sign Up to Human and Plant Disease Detection with Health and Physical fitness recommendation App dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]} hours. Please Log-in to your account.\n\nRegards: Vicky AI Production"""
        self.send_mail(email=email,message=message)
        self.log=add_logger()
        self.log.log(f'Sign-Up Sucessfully mail send to email: {str(email)}','emails.log',1)
    def failed_login_mail(self,email,email_validation_flag):
        '''Take the email address to send mail
        args: 
            email: email address of a user.'''
        dt=datetime.now()
        if email_validation_flag:
            message = f"""\
        Subject: Failed to Log-In

        Dear User:\n\t\tYour Password is invalid to log on to Human and Plant Disease Detection with Health and Physical fitness recommendation App dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]} hours. Please try again to Log-in on your account.\n\nRegards: Vicky AI Production"""
        else:
            message = f"""\
        Subject: Failed to Log-In

        Dear User:\n\t\tYour Email or Password is invalid to log on to Human and Plant Disease Detection with Health and Physical fitness recommendation App dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]} hours. Please try again to Log-in on your account Or if you are a new user then try to Sign Up.\n\nRegards: Vicky AI Production"""
        self.send_mail(email=email,message=message)
        self.log=add_logger()
        self.log.log(f'Failed to Log-In Sucessfully mail send to email: {str(email)}','emails.log',2)
    def send_code(self,code,email):
        '''Send code to the user for email verification
        args: 
            code: Code that will send to the user via email'''
        dt=datetime.now()
        message = f"""\
    Subject: Email Verification

    Dear User:\n\t\tYour code of verification is {code} to Human and Plant Disease Detection with Health and Physical fitness recommendation App dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]} hours. If you don't requested this then simply ignore it or contact us at vickyaiproduction@gmail.com'\n\nRegards: Vicky AI Production"""
        self.send_mail(email=email,message=message)
        self.log=add_logger()
        self.log.log(f'Email verification code send to email: {str(email)}','emails.log',2)
class send_mail_with_threading(Thread):
    def __init__(self,email,message):
        Thread.__init__(self)
        self.email=email
        self.message=message
        self.log=add_logger()
    def run(self):
        SENDER = 'vickyaiproduction@gmail.com'  
        RECIPIENT  = self.email
        email_password=os.environ.get('MAIL_PASSWORD')
        USERNAME_SMTP = os.environ.get('USERNAME_SMTP')
        PASSWORD_SMTP = os.environ.get('PASSWORD_SMTP')


        HOST = "email-smtp.us-east-2.amazonaws.com"
        PORT = 587
        self.log=add_logger()
        try:
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.ehlo()
            server.starttls()
            #stmplib docs recommend calling ehlo() before & after starttls()
            server.ehlo()
            server.login(SENDER, email_password)
            server.sendmail(SENDER, RECIPIENT, self.message)
            # server.sendmail(SENDER, RECIPIENT, msg.as_string())
            server.close()
            self.log.log(f'Sucessfully send the mail to {str(RECIPIENT)} by simple smtp protocol','emails.log',1)
        except Exception as e:
            self.log.log(f'Could not send the mail to {str(RECIPIENT)} by simple smtp protocol now trying with AWS SES services  error, {str(e)}','emails.log',3)
            try:  
                server = smtplib.SMTP(HOST, PORT)
                server.ehlo()
                server.starttls()
                #stmplib docs recommend calling ehlo() before & after starttls()
                server.ehlo()
                server.login(USERNAME_SMTP, PASSWORD_SMTP)
                server.sendmail(SENDER, RECIPIENT, self.message)
                # server.sendmail(SENDER, RECIPIENT, msg.as_string())
                server.close()
                self.log=add_logger()
                self.log.log(f'Sucessfully send the mail to {str(RECIPIENT)}','emails.log',1)
            # Display an error message if something goes wrong.
            except Exception as e:
                self.log.log(f'Cloud not send the mail to {str(RECIPIENT)} error, {str(e)}','emails.log',3)
            
            
        