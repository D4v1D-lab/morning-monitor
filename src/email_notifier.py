import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_ticket_summary(tickets_text):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "🎫 Your Jira Tickets Summary"

    body = MIMEText(tickets_text, "plain")
    msg.attach(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("Email sent successfully!")


if __name__ == "__main__":
    from src.jira_client import get_my_tickets, print_tickets_summary
    import io
    import sys

    response = get_my_tickets()

    #Captura el output de print_tickets_summary
    captured = io.StringIO()
    sys.stdout = captured
    print_tickets_summary(response)
    sys.stdout = sys.__stdout__

    tickets_text = captured.getvalue()
    send_ticket_summary(tickets_text)