import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to download a single file
def download_file(url, folder):
    response = requests.get(url)
    filename = os.path.join(folder, os.path.basename(url))
    
    with open(filename, 'wb') as file:
        file.write(response.content)

# Function to clone a webpage
def clone_page(url, folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Save the main page
    main_page = os.path.join(folder, 'index.html')
    with open(main_page, 'w') as file:
        file.write(str(soup))
    
    # Find all linked resources
    for tag in soup.find_all(['img', 'script', 'link']):
        attr = 'src' if tag.name == 'img' or tag.name == 'script' else 'href'
        resource_url = tag.get(attr)
        
        if resource_url:
            # Convert relative URLs to absolute URLs
            resource_url = urljoin(url, resource_url)
            
            # Download the resource
            download_file(resource_url, folder)

# Main function
def main():
    url = input("Enter the URL of the website to clone: ")
    folder = 'cloned_site'
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    clone_page(url, folder)
    print("Website cloned successfully!")

if __name__ == "__main__":
    main()
