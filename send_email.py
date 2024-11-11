import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")


def send_mail():

    sender_email = "noreplyahmetcol@gmail.com"
    sender_password = GMAIL_APP_PASS
    recipient_emails = ["colmuhterem@gmail.com", sender_email]
    subject = "Amazon Prices TXT Files"
    body = "See attachments"

    # Create the email message
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = sender_email
    # Attach the email body
    html_part = MIMEText(body, "plain")
    message.attach(html_part)

    # Attach multiple files
    attachments = ["buy_CA_sell_US.txt", "buy_US_sell_CA.txt"]
    for filename in attachments:
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
        except FileNotFoundError as e:
            print(e)
            break
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        message.attach(part)

    # Send the email with BCC
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_emails, message.as_string())


if __name__ == "__main__":
    send_mail()
