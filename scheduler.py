import schedule
import time
from jira_client import get_my_tickets, print_tickets_summary
from email_notifier import send_ticket_summary
import io
import sys

known_ticket_ids = set()

def get_tickets_text():
    response = get_my_tickets()
    captured = io.StringIO()
    sys.stdout = captured
    print_tickets_summary(response)
    sys.stdout = sys.__stdout__
    return captured.getvalue(), response.json().get("issues", [])

def daily_report():
    print("Running daily report...")
    text, _ = get_tickets_text()
    send_ticket_summary(text)

def check_new_tickets():
    global known_ticket_ids
    _, issues = get_tickets_text()
    current_ids = {issue["id"] for issue in issues}

    if not known_ticket_ids:
        known_ticket_ids = current_ids
        print("Initialized ticket tracking.")
        return

    new_ids = current_ids - known_ticket_ids
    if new_ids:
        print(f"New tickets detected: {new_ids}")
        text, _ = get_tickets_text()
        send_ticket_summary(text)
        known_ticket_ids = current_ids

if __name__ == "__main__":
    schedule.every().day.at("08:00").do(daily_report)
    schedule.every(1).minutes.do(check_new_tickets)

    print("Scheduler running...")
    while True:
        schedule.run_pending()
        time.sleep(30)