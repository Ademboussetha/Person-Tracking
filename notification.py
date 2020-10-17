""" 
Developed by : Adem Boussetha
Email : ademboussetha@gmail.com
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_mail(time):

    gmailUser = 'adamboussatha0@gmail.com'
    gmailPassword = "getthefuckout"
    recipient = 'ademboussetha@gmail.com'
    message='Un intrus est entrée à votre maison à : '+ time
    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = "Subject of the email"
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    print(f"notification sent to {gmailUser}")
    mailServer.close()