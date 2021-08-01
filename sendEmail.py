import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import configobj
import datetime
import os
config = configobj.ConfigObj('.env')
port = 2525
smtp_server = "smtp.mailtrap.io"
login = config['SMTP_USERNAME'] 
password = config['SMTP_PASSWORD'] 

sender_email = "mailtrap@example.com"
receiver_email = "new@example.com"



last_sent = datetime.datetime.now()

def timeFromLastSent():
    if(last_sent is None):
        return 10
    else:
        return (datetime.datetime.now() - last_sent).total_seconds()

# send your email
def send(index):
    global last_sent
    if(os.path.exists("./frame.jpg") and timeFromLastSent() >= 10):
        last_sent = datetime.datetime.now()
        encoded = base64.b64encode(open("frame.jpg", "rb").read()).decode()
        html = f"""\
        <html>
        <body>
            <img src="data:image/jpg;base64,{encoded}">
            <button onclick="window.open("localhost.com/{index}");">Gravar</button>
        </body>
        </html>
        """

        message = MIMEMultipart("alternative")
        message["Subject"] = "inline embedding"
        message["From"] = sender_email
        message["To"] = receiver_email

        part = MIMEText(html, "html")
        message.attach(part)
        
        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login(login, password)
            server.sendmail(
            sender_email, receiver_email, message.as_string() )
        print('Sent')
        return
