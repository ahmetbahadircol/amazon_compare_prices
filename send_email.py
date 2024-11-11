import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")

sender_email = "noreplyahmetcol@gmail.com"
sender_password = GMAIL_APP_PASS
recipient_email = "colmuhterem@gmail.com"
subject = "Amazon Prices TXT Files"
body = "See attachments"


with open("buy_CA_sell_US.txt", "rb") as attachment:
    # Add the attachment to the message
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename= 'attachment.txt'",
)

message = MIMEMultipart()
message["Subject"] = subject
message["From"] = sender_email
message["To"] = recipient_email
html_part = MIMEText(body)
message.attach(html_part)
message.attach(part)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message.as_string())
