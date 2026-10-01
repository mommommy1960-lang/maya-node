"""Host-run SMTP worker. Never enqueues or approves jobs."""
import json
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from .dispatch_queue import DispatchQueue


class MailSender:
    def __init__(self, host, username, password, port=465):
        if not host or not username or not password:
            raise ValueError('Mail configuration is incomplete')
        self.host, self.username, self.password, self.port = host, username, password, port

    def __call__(self, payload):
        msg = EmailMessage()
        msg['From'] = self.username
        msg['To'] = payload['recipient']
        msg['Subject'] = payload['subject']
        msg['Message-ID'] = make_msgid()
        msg.set_content(payload['body'])
        with smtplib.SMTP_SSL(self.host, self.port, timeout=30, context=ssl.create_default_context()) as smtp:
            smtp.login(self.username, self.password)
            refused = smtp.send_message(msg)
            if refused:
                raise RuntimeError('Recipient refused')
        return {'message_id': str(msg['Message-ID']), 'status': 'smtp_accepted'}


def main():
    # Configuration fails before any queue job is claimed.
    credential = Path(os.environ['CREDENTIALS_DIRECTORY']) / 'smtp_password'
    sender = MailSender(os.environ['MAYA_SMTP_HOST'], os.environ['MAYA_SMTP_USER'], credential.read_text().strip(), int(os.environ.get('MAYA_SMTP_PORT', '465')))
    queue = DispatchQueue(os.environ['MAYA_QUEUE_PATH'])
    alerts = []
    def alert(item):
        alerts.append(item)
        print(json.dumps({'alert': item}), flush=True)
    queue.run_once(sender, alert)
    print(json.dumps({'counts': queue.inspection()['counts']}), flush=True)
    if alerts:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
