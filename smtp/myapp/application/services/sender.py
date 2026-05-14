from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib


class EmailSender:
    def __init__(self, sender: str = "root@localhost"):
        self.sender = sender

    async def send(self, recipients: list = ["somebody@example.com"], subject: str = "Sent via aiosmtplib",):
        message = MIMEMultipart("alternative")
        message["From"] = self.sender
        message["To"] = recipients[0]

        plain_text_message = MIMEText("Подтверждение почты", "plain", "utf-8")
        html_message = MIMEText(
            f"""
            <html>
            <body>
            Ваш код подтверждения:
            <h1>{subject}</h1>
            </body>
            </html>""", "html", "utf-8"
        )
        message.attach(plain_text_message)
        message.attach(html_message)

        await aiosmtplib.send(
            message,
            sender=self.sender,
            recipients=recipients,
            hostname="maildev",
            port=1025
        )
