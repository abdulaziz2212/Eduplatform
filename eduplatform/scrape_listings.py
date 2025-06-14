import requests
from bs4 import BeautifulSoup
import time
import csv
import json
from urllib.parse import urljoin, urlparse
import random

class OLXScraper:
    def __init__(self):
        self.base_url = "https://www.olx.uz"
        self.session = requests.Session()
        
        # Headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_page(self, url, retries=3):
        """Fetch a page with error handling and retries"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(2, 5))
                else:
                    print(f"Failed to fetch {url} after {retries} attempts")
                    return None
    
    def parse_listing(self, listing_element):
        """Parse individual listing from search results"""
        try:
            data = {}
            
            # Title
            title_elem = listing_element.find('h6') or listing_element.find('h4')
            data['title'] = title_elem.get_text(strip=True) if title_elem else 'N/A'
            
            # Price
            price_elem = listing_element.find('p', {'data-testid': 'ad-price'}) or \
                        listing_element.find('span', class_=lambda x: x and 'price' in x.lower())
            data['price'] = price_elem.get_text(strip=True) if price_elem else 'N/A'
            
            # Location
            location_elem = listing_element.find('span', {'data-testid': 'location-date'}) or \
                           listing_element.find('p', class_=lambda x: x and 'location' in x.lower())
            data['location'] = location_elem.get_text(strip=True) if location_elem else 'N/A'
            
            # Link
            link_elem = listing_element.find('a')
            if link_elem and link_elem.get('href'):
                data['url'] = urljoin(self.base_url, link_elem['href'])
            else:
                data['url'] = 'N/A'
            
            # Image
            img_elem = listing_element.find('img')
            data['image_url'] = img_elem.get('src') if img_elem else 'N/A'
            
            return data
        except Exception as e:
            print(f"Error parsing listing: {e}")
            return None
    
    def scrape_search_results(self, search_url, max_pages=5):
        """Scrape multiple pages of search results"""
        all_listings = []
        
        for page in range(1, max_pages + 1):
            print(f"Scraping page {page}...")
            
            # Construct page URL
            if '?' in search_url:
                page_url = f"{search_url}&page={page}"
            else:
                page_url = f"{search_url}?page={page}"
            
            response = self.get_page(page_url)
            if not response:
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find listing containers (these selectors may need adjustment)
            listings = soup.find_all(['div', 'li'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['listing', 'ad-', 'offer-wrapper']
            ))
            
            if not listings:
                # Try alternative selectors
                listings = soup.find_all('div', {'data-cy': 'l-card'}) or \
                          soup.find_all('div', class_=lambda x: x and 'card' in x.lower())
            
            if not listings:
                print(f"No listings found on page {page}")
                break
            
            page_listings = []
            for listing in listings:
                parsed_listing = self.parse_listing(listing)
                if parsed_listing:
                    page_listings.append(parsed_listing)
            
            if not page_listings:
                print(f"No valid listings found on page {page}")
                break
            
            all_listings.extend(page_listings)
            print(f"Found {len(page_listings)} listings on page {page}")
            
            # Be respectful with requests
            time.sleep(random.uniform(1, 3))
        
        return all_listings
    
    def scrape_listing_details(self, listing_url):
        """Scrape detailed information from individual listing page"""
        response = self.get_page(listing_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        details = {}
        
        try:
            # Title
            title = soup.find('h1') or soup.find('h2')
            details['title'] = title.get_text(strip=True) if title else 'N/A'
            
            # Price
            price = soup.find('h3') or soup.find('span', class_=lambda x: x and 'price' in x.lower())
            details['price'] = price.get_text(strip=True) if price else 'N/A'
            
            # Description
            desc = soup.find('div', class_=lambda x: x and 'description' in x.lower()) or \
                   soup.find('div', {'data-cy': 'ad_description'})
            details['description'] = desc.get_text(strip=True) if desc else 'N/A'
            
            # Contact info
            phone = soup.find('a', href=lambda x: x and 'tel:' in x)
            details['phone'] = phone.get_text(strip=True) if phone else 'N/A'
            
            # Additional parameters
            params = soup.find_all('div', class_=lambda x: x and 'param' in x.lower())
            details['parameters'] = {}
            for param in params:
                key_elem = param.find('span', class_=lambda x: x and 'key' in x.lower())
                val_elem = param.find('span', class_=lambda x: x and 'value' in x.lower())
                if key_elem and val_elem:
                    details['parameters'][key_elem.get_text(strip=True)] = val_elem.get_text(strip=True)
            
        except Exception as e:
            print(f"Error scraping listing details: {e}")
        
        return details
    
    def save_to_csv(self, data, filename='olx_listings.csv'):
        """Save scraped data to CSV file"""
        if not data:
            print("No data to save")
            return
        
        fieldnames = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")
    
    def save_to_json(self, data, filename='olx_listings.json'):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")

# Example usage
def main():
    scraper = OLXScraper()
    
    # Example: Search for cars
    search_url = "https://www.olx.uz/transport/legkovye-avtomobili/"
    
    # Scrape search results
    print("Starting to scrape OLX.uz...")
    listings = scraper.scrape_search_results(search_url, max_pages=3)
    
    if listings:
        print(f"Successfully scraped {len(listings)} listings")
        
        # Save data
        scraper.save_to_csv(listings)
        scraper.save_to_json(listings)
        
        # Example: Get detailed info for first few listings
        print("\nScraping detailed information for first 3 listings...")
        for i, listing in enumerate(listings[:3]):
            if listing['url'] != 'N/A':
                print(f"Scraping details for listing {i+1}...")
                details = scraper.scrape_listing_details(listing['url'])
                if details:
                    print(f"Title: {details['title']}")
                    print(f"Price: {details['price']}")
                    print(f"Description: {details['description'][:100]}...")
                    print("-" * 50)
                time.sleep(2)
    else:
        print("No listings found")

if __name__ == "__main__":
    main()