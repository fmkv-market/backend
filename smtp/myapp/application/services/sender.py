from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from myapp.application.interface.sender import ISender


class EmailSender(ISender):
    def __init__(self, sender: str = "root@localhost"):
        self.sender = sender

    async def send(self, recipients: list = ["somebody@example.com"], subject: str = "Confirmation") -> None:
        content = MIMEMultipart("alternative")
        content["From"] = self.sender
        content["To"] = recipients[0]
        content["Subject"] = subject

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
        content.attach(plain_text_message)
        content.attach(html_message)

        await aiosmtplib.send(
            content,
            sender=self.sender,
            recipients=recipients,
            hostname="maildev",
            port=1025
        )

