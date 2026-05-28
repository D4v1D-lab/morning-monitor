import requests
import smtplib
import pytest
from unittest.mock import patch, Mock
from src.jira_client import get_my_tickets, print_tickets_summary
from src.email_notifier import send_ticket_summary
from src import scheduler


def test_get_my_tickets_returns_200():
    with patch("src.jira_client.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = get_my_tickets()

        assert response.status_code == 200

def test_get_my_tickets_returns_401():
    with patch("src.jira_client.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        response = get_my_tickets()

        assert response.status_code == 401

def test_get_my_tickets_returns_404():
    with patch("src.jira_client.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = get_my_tickets()

        assert response.status_code == 404

def test_get_my_tickets_returns_500():
    with patch("src.jira_client.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response = get_my_tickets()

        assert response.status_code == 500

def test_get_my_tickets_returns_error():
    with patch("src.jira_client.requests.get") as mock_get:

        mock_get.side_effect = requests.exceptions.ConnectionError

        with pytest.raises(requests.exceptions.ConnectionError):
            get_my_tickets()

def test_no_tickets_shows_empty_message(capsys):
    mock_response = Mock()
    mock_response.json.return_value = {"issues": []}

    print_tickets_summary(mock_response)

    captured = capsys.readouterr()
    assert "No tickets assigned to you so far today" in captured.out
    assert "Total tickets: 0" in captured.out


def test_send_ticket_summary_success():
    with patch("src.email_notifier.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_ticket_summary("Test summary")

        mock_smtp.assert_called_once_with("smtp.gmail.com", 465)
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()


def test_send_ticket_summary_auth_error():
    with patch("src.email_notifier.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = Mock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, b"auth failed")
        mock_smtp.return_value.__enter__.return_value = mock_server

        with pytest.raises(smtplib.SMTPAuthenticationError):
            send_ticket_summary("Test summary")


def test_send_ticket_summary_connection_error():
    with patch("src.email_notifier.smtplib.SMTP_SSL") as mock_smtp:
        mock_smtp.side_effect = smtplib.SMTPConnectError(421, "connection failed")

        with pytest.raises(smtplib.SMTPConnectError):
            send_ticket_summary("Test summary")


def test_daily_report_sends_email():
    with patch("src.scheduler.get_my_tickets") as mock_get, \
         patch("src.scheduler.send_ticket_summary") as mock_send:

        mock_response = Mock()
        mock_response.json.return_value = {
            "issues": [
                {
                    "id": "10001", "key": "PROJ-1",
                    "fields": {
                        "summary": "Test", "status": {"name": "To Do"},
                        "priority": {"name": "Medium"}, "created": "2026-05-27T10:00:00"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        scheduler.daily_report()

        mock_send.assert_called_once()


def test_check_new_tickets_first_run():
    with patch("src.scheduler.get_my_tickets") as mock_get, \
         patch("src.scheduler.send_ticket_summary") as mock_send:

        mock_response = Mock()
        mock_response.json.return_value = {
            "issues": [
                {
                    "id": "10001", "key": "PROJ-1",
                    "fields": {
                        "summary": "Test", "status": {"name": "To Do"},
                        "priority": {"name": "Medium"}, "created": "2026-05-27T10:00:00"
                    }
                },
                {
                    "id": "10002", "key": "PROJ-2",
                    "fields": {
                        "summary": "Test 2", "status": {"name": "Done"},
                        "priority": {"name": "High"}, "created": "2026-05-27T11:00:00"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        scheduler.known_ticket_ids = set()
        scheduler.check_new_tickets()

        mock_send.assert_not_called()
        assert scheduler.known_ticket_ids == {"10001", "10002"}


def test_check_new_tickets_detects_new():
    with patch("src.scheduler.get_my_tickets") as mock_get, \
         patch("src.scheduler.send_ticket_summary") as mock_send:

        mock_response = Mock()
        mock_response.json.return_value = {
            "issues": [
                {
                    "id": "10001", "key": "PROJ-1",
                    "fields": {
                        "summary": "Test", "status": {"name": "To Do"},
                        "priority": {"name": "Medium"}, "created": "2026-05-27T10:00:00"
                    }
                },
                {
                    "id": "10002", "key": "PROJ-2",
                    "fields": {
                        "summary": "Test 2", "status": {"name": "Done"},
                        "priority": {"name": "High"}, "created": "2026-05-27T11:00:00"
                    }
                },
                {
                    "id": "10003", "key": "PROJ-3",
                    "fields": {
                        "summary": "New Ticket", "status": {"name": "Open"},
                        "priority": {"name": "Low"}, "created": "2026-05-27T12:00:00"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        scheduler.known_ticket_ids = {"10001", "10002"}
        scheduler.check_new_tickets()

        mock_send.assert_called_once()
        assert scheduler.known_ticket_ids == {"10001", "10002", "10003"}