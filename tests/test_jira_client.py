import requests
import smtplib
import pytest
from unittest.mock import patch, Mock
from jira_client import get_my_tickets, print_tickets_summary
from email_notifier import send_ticket_summary


def test_get_my_tickets_returns_200():
    with patch("jira_client.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = get_my_tickets()

        assert response.status_code == 200

def test_get_my_tickets_returns_401():
    with patch("jira_client.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        response = get_my_tickets()

        assert response.status_code == 401

def test_get_my_tickets_returns_404():
    with patch("jira_client.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = get_my_tickets()

        assert response.status_code == 404

def test_get_my_tickets_returns_500():
    with patch("jira_client.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response = get_my_tickets()

        assert response.status_code == 500

def test_get_my_tickets_returns_error():
    with patch("jira_client.requests.get") as mock_get:

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
    with patch("email_notifier.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_ticket_summary("Test summary")

        mock_smtp.assert_called_once_with("smtp.gmail.com", 465)
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()


def test_send_ticket_summary_auth_error():
    with patch("email_notifier.smtplib.SMTP_SSL") as mock_smtp:
        mock_server = Mock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, b"auth failed")
        mock_smtp.return_value.__enter__.return_value = mock_server

        with pytest.raises(smtplib.SMTPAuthenticationError):
            send_ticket_summary("Test summary")


def test_send_ticket_summary_connection_error():
    with patch("email_notifier.smtplib.SMTP_SSL") as mock_smtp:
        mock_smtp.side_effect = smtplib.SMTPConnectError(421, "connection failed")

        with pytest.raises(smtplib.SMTPConnectError):
            send_ticket_summary("Test summary")