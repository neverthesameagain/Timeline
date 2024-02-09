from bs4 import BeautifulSoup
import requests
import re

def datefor(text):
    date_pattern = r'\b(?:\d{4}-\d{2}-\d{2}|\d{4})\b'
    matches = re.findall(date_pattern, text)
    return matches

url = input("Enter the webpage to get an interactive Timeline of: ")
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

paragraphs = []
images = []
link = []
heading = []
remaining_content = []

for tag in soup.find_all():
    if tag.name == "p":
        paragraphs.append(tag.text)
    elif tag.name == "img":
        images.append(url + tag['src'])
    elif tag.name == "a":
        if "href" in tag.attrs:
            if "https://en.wikipedia.org/w/" not in tag['href']:
                link.append(url + tag['href'])
            else:
                link.append(tag['href'])
    elif tag.name.startswith("h"):
        heading.append(tag.text)
    else:
        remaining_content.append(tag.text)
print(paragraphs)


timeline_data = []
for paragraph in paragraphs:
    dates = datefor(paragraph)
    if dates:
        for date in dates:
            description = paragraph.replace(date, '').strip()
            timeline_data.append((date, description))

timeline_data.sort(key=lambda x: x[0])

for date, description in timeline_data:
    print(f"Date/Year: {date}")
    print(f"Description: {description}\n")

