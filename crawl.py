import json
import requests
from bs4 import BeautifulSoup

# Define function to save URL and HTML content to CSV
def save_to_json(url, html):
    data = {
        'url': url,
        'html': html
    }

    with open('crawled.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

link_list = []
visited_urls = []

# Define the crawl function
def crawl(url, depth=0, max_depth=3):
    if depth > max_depth:
        return
    if url in visited_urls:
        return
    visited_urls.append(url)

    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        print("Title: ", soup.title.string)
        print("URL: ", url)

        save_to_json(url, html[0:100])

    for link in soup.find_all('a'):
        absolute_url = link.get('href')
        if absolute_url is None:
            continue
        elif absolute_url.startswith('http') or absolute_url.startswith('https'):
            link_list.append(absolute_url)
            crawl(absolute_url, depth + 1, max_depth)
        else:
            newUrl = url + absolute_url
            link_list.append(newUrl)
            crawl(newUrl, depth + 1, max_depth)

url = "https://www.youtube.com"
crawl(url)

print(link_list)