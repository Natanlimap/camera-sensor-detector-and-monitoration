import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import configobj
config = configobj.ConfigObj('.env')

port = 2525
smtp_server = "smtp.mailtrap.io"
login = config['SMTP_USERNAME'] 
password = config['SMTP_PASSWORD'] 

sender_email = "mailtrap@example.com"
receiver_email = "new@example.com"
message = MIMEMultipart("alternative")
message["Subject"] = "inline embedding"
message["From"] = sender_email
message["To"] = receiver_email

# We assume that the image file is in the same directory that you run your Python script from
encoded = base64.b64encode(open("frame.jpg", "rb").read()).decode()

html = f"""\
<html>
 <body>
     <img src="data:image/jpg;base64,{encoded}">
    <button>Gravar</button>
 </body>
</html>
"""

part = MIMEText(html, "html")
message.attach(part)

# send your email
with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
   server.login(login, password)
   server.sendmail(
       sender_email, receiver_email, message.as_string()
   )
print('Sent')