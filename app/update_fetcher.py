import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from app.models import SoftwareTool, Update
from app import db, scheduler


def fetch_updates_for_tool(software_tool):
    if software_tool.update_source == "api":
        return fetch_updates_from_api(software_tool)
    elif software_tool.update_source == "rss":
        return fetch_updates_from_rss(software_tool)
    elif software_tool.update_source == "scrape":
        return fetch_updates_from_scrape(software_tool)
    else:
        print(f"Unknown update source for {software_tool.name}")
        return []


def fetch_updates_from_api(software_tool):
    # Mock data for testing
    updates = [
        {
            "version": "1.0.0",
            "release_date": datetime(2023, 1, 1),
            "raw_notes": "Initial release of API-based tool.",
        },
        {
            "version": "1.1.0",
            "release_date": datetime(2023, 2, 1),
            "raw_notes": "Added new API endpoints.",
        },
    ]
    return updates


def fetch_updates_from_rss(software_tool):
    # Mock data for testing
    updates = [
        {
            "version": "2.0.0",
            "release_date": datetime(2023, 3, 1),
            "raw_notes": "Major overhaul with new features.",
        },
        {
            "version": "2.1.0",
            "release_date": datetime(2023, 4, 1),
            "raw_notes": "Minor improvements and bug fixes.",
        },
    ]
    return updates


def fetch_updates_from_scrape(software_tool):
    # Mock data for testing
    updates = [
        {
            "version": "3.0.0",
            "release_date": datetime(2023, 5, 1),
            "raw_notes": "New UI design and performance enhancements.",
        },
        {
            "version": "3.1.0",
            "release_date": datetime(2023, 6, 1),
            "raw_notes": "Security patches and stability improvements.",
        },
    ]
    return updates


# def fetch_updates_from_api(software_tool):
#     # Placeholder for API fetching logic
#     # Implement API requests based on the software tool's API
#     updates = []
#     # Example: response = requests.get(software_tool.update_url)
#     # Parse the response and extract updates
#     return updates


# def fetch_updates_from_rss(software_tool):
#     updates = []
#     feed = feedparser.parse(software_tool.update_url)
#     for entry in feed.entries:
#         update = {
#             "version": entry.title,
#             "release_date": datetime(*entry.published_parsed[:6]),
#             "raw_notes": entry.summary,
#         }
#         updates.append(update)
#     return updates


# def fetch_updates_from_scrape(software_tool):
#     updates = []
#     response = requests.get(software_tool.update_url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     # Implement parsing logic specific to the website structure
#     # For example:
#     # for item in soup.find_all('div', class_='update'):
#     #     update = {
#     #         'version': item.find('h2').text,
#     #         'release_date': parse_date(item.find('span', class_='date').text),
#     #         'raw_notes': item.find('p', class_='notes').text,
#     #     }
#     #     updates.append(update)
#     return updates


def fetch_all_updates():
    software_tools = SoftwareTool.query.all()
    for tool in software_tools:
        print(f"Fetching updates for {tool.name}")
        updates = fetch_updates_for_tool(tool)
        for update_data in updates:
            # Check if the update already exists
            existing_update = Update.query.filter_by(
                software_id=tool.id, version=update_data["version"]
            ).first()
            if existing_update:
                continue  # Skip existing updates
            # Create a new Update instance
            new_update = Update(
                software_id=tool.id,
                version=update_data["version"],
                release_date=update_data["release_date"],
                raw_notes=update_data["raw_notes"],
            )
            db.session.add(new_update)
        db.session.commit()
