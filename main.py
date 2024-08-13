# Import necessary libraries
import time
import requests
from bs4 import BeautifulSoup
from collections import deque
import logging
import pandas as pd

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Te Starting point for the BFS crawler
starting_url = "https://quotes.toscrape.com/"

# Store the data and process the queue
queue = deque([starting_url])
visited = set()
depth = {starting_url: 0}


# Function that will take each url and return the contents with bs4 parser
def fetch_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'lxml')


# Crawling process
# While loop will run as long as there is an item inside the queue, it will pick the next url to process again until it is empty
try:
    while queue:
        max_depth = 3
        current_url = queue.popleft()
        current_depth = depth[current_url]
    # The depth of our search is 3-level, so the 'if statement' checks if we are still within the required depth
        if current_depth < max_depth:
            soup = fetch_page(current_url)
            for link in soup.find_all('a', href=True):
                url = link['href']
                # Joining short URL with the incomplete scrapped link
                if url.startswith('/'):
                    url = starting_url + url
                    if url not in visited:
                        visited.add(url)
                        queue.append(url)
                        depth[url] = current_depth + 1
            time.sleep(2)
        time.sleep(2)
        logging.info(f'Successfully fetched data from {current_url}')
except Exception as e:
    print(f'Error fetching {current_url}: {e}')

# Save links to CSV file named 'data'
df = pd.DataFrame(visited)
df.to_csv("data.csv", index=False, header=False)
print("Finished")