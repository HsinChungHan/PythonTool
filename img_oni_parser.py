from bs4 import BeautifulSoup

def extract_urls_from_html(file_path):
    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Find all div elements with class 'image_item_url'
    divs = soup.find_all('div', class_='image_item_url')

    # Extract the URLs from the 'href' attribute of the 'a' tags within the divs
    urls = [a['href'] for div in divs for a in div.find_all('a', href=True)]
    
    # Convert the list of URLs to a string, where each URL is enclosed in quotes and separated by commas
    urls_str = ', '.join(f'"{url}"' for url in urls)
    
    return urls_str

path = '/Users/chunghanhsin/Downloads/PDF to PNG macOS.html'
print(extract_urls_from_html(path))
