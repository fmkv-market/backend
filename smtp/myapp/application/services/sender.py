from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from myapp.application.interface.sender import ISender


class EmailSender(ISender):
    def __init__(self, sender: str = "root@localhost"):
        self.sender = sender

    async def send(self, recipients: list = ["somebody@example.com"], message: str = "Sent via aiosmtplib",) -> None:
        content = MIMEMultipart("alternative")
        content["From"] = self.sender
        content["To"] = recipients[0]

        plain_text_message = MIMEText("Подтверждение почты", "plain", "utf-8")
        html_message = MIMEText(
            f"""
            <html>
            <body>
            Ваш код подтверждения:
            <h1>{message}</h1>
            </body>
            </html>""", "html", "utf-8"
        )
        content.attach(plain_text_message)
        content.attach(html_message)

        await aiosmtplib.send(
            message,
            sender=self.sender,
            recipients=recipients,
            hostname="maildev",
            port=1025
        )



class SmsSender(ISender):
    """
    Стратегия отправки через SMS-шлюз (stub-реализация).
    В продакшне здесь — вызов API провайдера (Twilio, SMSC и др.)
    """

    def __init__(self, api_url: str = "http://sms-gateway/send", api_key: str = ""):
        self.api_url = api_url
        self.api_key = api_key

    async def send(self, recipients: list[str], message: str) -> None:
        async with aiohttp.ClientSession() as session:
            for phone in recipients:
                await session.post(
                    self.api_url,
                    json={"phone": phone, "text": message},
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )

