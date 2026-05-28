from dotenv import load_dotenv
import os

load_dotenv()

JIRA_URL= os.getenv("JIRA_URL")
JIRA_EMAIL= os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN= os.getenv("JIRA_API_TOKEN")

EMAIL_SENDER= os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD= os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER= os.getenv("EMAIL_RECEIVER")