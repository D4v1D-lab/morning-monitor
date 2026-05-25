import requests
from config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN


def get_my_tickets():
    url = f"{JIRA_URL}/rest/api/3/search/jql"

    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    headers = {
        "Accept": "application/json"
    }

    params = {
        "jql": "assignee = currentUser() ORDER BY created DESC",
        "maxResults": 50,
        "fields": "summary,status,priority,assignee,created"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)

    return response


def print_tickets_summary(response):
    data = response.json()
    issues = data.get("issues", [])

    print(f"\n📋 Total tickets: {len(issues)}\n")

    if len(issues) == 0:
        print("No tickets assigned to you so far today")
    else:
        for issue in issues:
            key = issue["key"]
            fields = issue["fields"]
            summary = fields["summary"]
            status = fields["status"]["name"]
            priority = fields["priority"]["name"] if fields["priority"] else "No priority"
            created = fields["created"][:10]

            print(f"🎫 {key} | {status} | {priority} | {created}")
            print(f"   {summary}")
            print()


if __name__ == "__main__":
    response = get_my_tickets()
    print(f"Status code: {response.status_code}")
    print_tickets_summary(response)