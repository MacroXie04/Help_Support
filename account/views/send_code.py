import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from sys import exception


def send_email(to_email, subject, message_body):
    # email server information
    smtp_server = "smtp.qiye.163.com"
    smtp_port = 465
    sender_email = "no_reply@helpandsupport.online"
    password = 'dG[FB=]h4^#}q"yD'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        raise exception(f"Error: {e}")



def sent_verification_code(to_email):
    # generate verification code
    code = random.randint(100000, 999999)

    # email message information
    subject = "Team Help and Support - Verification Code"
    message_body = f"You are receiving this email because you have requested a verification code and code will expire in five minutes. Your verification code is: {code}"

    if send_email(to_email, subject, message_body):
        return code


