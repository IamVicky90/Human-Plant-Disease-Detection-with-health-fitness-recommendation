import smtplib, ssl
from datetime import datetime
import os
class mail:
    def __init__(self)->None:
        pass
    def send_mail(self,email,message)->None:
        '''
        To send email to specific email address
        params: 
            email: email address of the reciever.
            message: Message to send the reciever.
        '''
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "vickyaiproduction@gmail.com"  # Enter your address
        receiver_email = email  # Enter receiver address
        password = os.environ.get('MAIL_PASSWORD')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    def user_login_mail(self,email):
        '''Take the email address to send mail
        args: 
            email: email address of a user.'''
        dt=datetime.now()
        message = f"""\
    Subject: Log-in Alert

    Dear User:\n\t\tYou have successfully logged on to Human and Plant Disease Detection with Health and Physical fitness recommendation App dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]} hours.\n\nRegards: Vicky AI Production"""
        self.send_mail(email=email,message=str(message))
    def user_signup_confirmation_mail(self,email):
        '''Take the email address to send mail
        args: 
            email: email address of a user.'''
        dt=datetime.now()
        message = f"""\
    Subject: Sign-Up Sucessfully

    Dear User:\n\t\tYou have successfully Sign Up to Human and Plant Disease Detection with Health and Physical fitness recommendation App dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]} hours. Please Log-in to your account.\n\nRegards: Vicky AI Production"""
        self.send_mail(email=email,message=str(message))
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
        self.send_mail(email=email,message=str(message))
    def send_code(self,code,email):
        '''Send code to the user for email verification
        args: 
            code: Code that will send to the user via email'''
        dt=datetime.now()
        message = f"""\
    Subject: Sign-Up Sucessfully

    Dear User:\n\t\tYour code of verification is {code} to Human and Plant Disease Detection with Health and Physical fitness recommendation App dated: {dt.strftime('%Y-%m-%d')}, time: {str(dt.timetz()).split('.')[0]} hours. If you don't requested this then simply ignore it or contact us at vickyaiproduction@gmail.com'\n\nRegards: Vicky AI Production"""
        self.send_mail(email=email,message=str(message))
            
            
        