import smtplib, ssl
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
        password = '<password>'
        # message = """\
        # Subject: Hi there

        # This message is sent from Python."""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)