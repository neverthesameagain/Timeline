import requests
from bs4 import BeautifulSoup
import re
import datetime
from dateutil.parser import parse
import json
from collections import defaultdict
import plotly.express as px

def get_event_data(query):
    """Scrape event data from the web and compile it into a list of dictionaries."""
    url = f"https://www.google.com/search?q={query}+timeline"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    timeline_blocks = soup.find_all("div", class_="yuRUbf")
    events = []
    for block in timeline_blocks:
        date_str = block.find("div", class_="fP1Qef").text.strip()
        date_match = re.match(r"(\w+\s+\d+,\s+\d{4})", date_str)
        if date_match:
            date = datetime.datetime.strptime(date_match.group(1), "%B %d, %Y")
        event_str = block.find("div", class_="DY5T1d").text.strip()
        event_match = re.search(r"(.*?)\s*\-\s*(.*?)\s*$", event_str)
        if event_match:
            event = {
                "date": date,
                "event": event_match.group(1).strip(),
                "description": event_match.group(2).strip(),
            }
            events.append(event)
    return events

def sort_events(events):
    """Sort events by date."""
    events.sort(key=lambda x: x["date"])
    return events

def visualize_timeline(events):
    """Create an interactive timeline using Plotly."""
    df = defaultdict(list)
    for event in events:
        df["Date"].append(event["date"].strftime("%Y-%m-%d"))
        df["Event"].append(event["event"])
        df["Description"].append(event["description"])
    fig = px.timeline(df, x_start="Date", x_end="Date", y="Event", color="Event", text="Description")
    fig.show()

if __name__ == "__main__":
    query = input("Enter a historical event: ")
    events = get_event_data(query)
    events = sort_events(events)
    visualize_timeline(events)
