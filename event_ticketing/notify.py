import smtplib, ssl, base64
from email.message import EmailMessage
from email.utils import make_msgid
from event_ticketing import settings

def send_mail(to: str, subject: str, html_body: str,
              png_b64: str | None = None,         
              text_body: str | None = None):

    msg = EmailMessage()
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(text_body or "Ваш почтовый клиент не поддерживает HTML.")
    msg.add_alternative(html_body, subtype="html")

    # --- если есть QR-картинка ---
    if png_b64:
        cid = make_msgid(domain="ticket.local")[1:-1]   
        html_body = html_body.replace("cid:qr.png", f"cid:{cid}")
        msg.get_payload()[1].set_content(html_body, subtype="html")

        png_bytes = base64.b64decode(png_b64)
        msg.get_payload()[1].add_related(png_bytes,
                                         maintype="image",
                                         subtype="png",
                                         cid=f"<{cid}>")

    # --- отправка ---
    ctx = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
        s.starttls(context=ctx)
        s.login(settings.SMTP_USER, settings.SMTP_PASS)
        s.send_message(msg)
