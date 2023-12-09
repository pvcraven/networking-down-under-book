"""
Example showing how to read in from a web page
"""

from bs4 import BeautifulSoup
import urllib.request

# Read in the web page
url_address = "http://thehill.com"
page = urllib.request.urlopen(url_address)

# Parse the web page
soup = BeautifulSoup(page.read(), "html.parser")

# Get a list of level 4 headings in the page
headings = soup.findAll("h4")

# Loop through each heading
for heading in headings:
    print(heading.text.strip())
