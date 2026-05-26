# 🌅 Morning Monitor

> Automated Jira ticket monitoring system that keeps you informed about your daily workload.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![Jira](https://img.shields.io/badge/Jira-REST%20API%20v3-0052CC?style=flat-square&logo=jira)
![pytest](https://img.shields.io/badge/pytest-passing-green?style=flat-square&logo=pytest)
![Status](https://img.shields.io/badge/status-complete-brightgreen?style=flat-square)

---

## 🚀 Features

| | Feature | Status |
|---|---|---|
| ✅ | Jira REST API integration | Done |
| ✅ | Automated email reports via Gmail | Done |
| ✅ | Unit tests with mocks — 9 scenarios | Done |
| ✅ | Secure credential management via `.env` | Done |
| ✅ | Scheduled execution via scheduler | Done |
| ✅ | Real-time new ticket detection | Done |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.14 | Core language |
| Jira REST API v3 | Ticket data source |
| smtplib | Email automation |
| schedule | Task scheduling |
| pytest + unittest.mock | Automated testing |
| python-dotenv | Secure credential management |

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/morning-monitor.git
cd morning-monitor
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your@email.com
JIRA_API_TOKEN=your_jira_api_token
EMAIL_SENDER=your.sender@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=your.receiver@gmail.com
> ⚠️ Never commit your `.env` file. It is protected by `.gitignore`.

---

## ▶️ How to Run

```bash
# Get your Jira tickets summary
python jira_client.py

# Send email report
python email_notifier.py

# Start scheduled monitoring (daily report + real-time new ticket detection)
python scheduler.py

# Run automated tests
pytest tests/ -v
```

---

## 🧪 Test Coverage

| Test | Description | Status |
|---|---|---|
| `test_get_my_tickets_returns_200` | Validates successful Jira connection | ✅ PASS |
| `test_get_my_tickets_returns_401` | Handles unauthorized access | ✅ PASS |
| `test_get_my_tickets_returns_404` | Handles resource not found | ✅ PASS |
| `test_get_my_tickets_returns_500` | Handles internal server error | ✅ PASS |
| `test_get_my_tickets_returns_error` | Handles no internet connection | ✅ PASS |
| `test_no_tickets_shows_empty_message` | Validates empty state message | ✅ PASS |
| `test_send_ticket_summary_success` | Validates successful email send | ✅ PASS |
| `test_send_ticket_summary_auth_error` | Handles SMTP authentication failure | ✅ PASS |
| `test_send_ticket_summary_connection_error` | Handles SMTP connection failure | ✅ PASS |

---

## 🗺️ Roadmap

- [x] Jira API integration
- [x] Automated email notifications
- [x] Unit tests with mocks
- [x] Scheduled execution via scheduler
- [x] Real-time new ticket detection

---

## 👨‍💻 Author

**David Patricio Martínez Hinojosa**
QA Automation Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/YOUR_LINKEDIN)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/YOUR_USERNAME)  