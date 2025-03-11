import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.application.port.email_service_port import EmailService


class SmtpEmailService(EmailService):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, to_email: str, subject: str, message: str) -> None:
        print('📧 Sending email...')
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        try:
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, to_email, msg.as_string())
            server.quit()
            print(f'Email sent to {to_email}')
        except Exception as e:
            print(f'Failed to send email: {e}')
