import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_sidebar_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a", class_="md-nav__link")  # Finds all links in navigation
    return [(link.get_text(strip=True), link['href']) for link in links if link['href'] and not link['href'].startswith('#')]

def write_to_file(filename, title, text):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Title: {title}\nContent:\n{text}\n")
        file.write("-" * 40 + "\n")  # Separator between entries

def main(base_url, start_path, output_file):
    full_url = f"{base_url}{start_path}"
    html = fetch_html(full_url)
    if html:
        links = parse_sidebar_links(html)
        for title, path in links:
            link = f"{base_url}{path}"
            print(f"Fetching content from {title} at {link}")
            page_html = fetch_html(link)
            if page_html:
                soup = BeautifulSoup(page_html, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
                write_to_file(output_file, title, text)

# Example usage, replace `base_url` and `start_path` with your initial page to scrape
main('https://django-ninja.dev/', '/', 'combined_text.txt')
