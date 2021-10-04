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