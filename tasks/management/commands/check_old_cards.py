import requests
import os
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

NOTION_API_URL = os.getenv("NOTION_API_URL")
NOTION_API_UPDATE_URL = os.getenv("NOTION_API_UPDATE_URL")
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_VERSION = os.getenv("NOTION_VERSION")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

class Command(BaseCommand):
    help = 'Identify old cards and update their status'
    def handle(self, *args, **kwargs):
        days_ago = datetime.now() - timedelta(days=int(os.getenv("DAYS")))

        # Query the Notion database
        response = requests.post(
            NOTION_API_URL.format(database_id=DATABASE_ID),
            headers=HEADERS,
            json={
                "filter": {
                    "and": [
                        {
                            "property": "Stage",
                            "select": {
                                "equals": "Lead"
                            }
                        },
                        {
                            "property": "Last edited time",
                            "last_edited_time": {
                                "before": days_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            }
                        }
                    ]
                }
            }
        )

        data = response.json()
        for result in data.get("results", []):
            page_id = result["id"]
            company_name = result["properties"]["Name"]["title"][0]["plain_text"]
            update_response = requests.patch(
                NOTION_API_UPDATE_URL.format(page_id=page_id),
                headers=HEADERS,
                json={
                    "properties": {
                        "Stage": {
                            "select": {
                                "name": "No response"
                            }
                        }
                    }
                }
            )
            if update_response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f'Task {page_id} {company_name} marked as no response'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to update task {page_id} {company_name}'))
