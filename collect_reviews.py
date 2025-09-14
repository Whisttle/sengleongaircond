import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import json
import time
import re

class GoogleReviewsScraper:
    def __init__(self, headless=True, timeout=30000):
        self.headless = headless
        self.timeout = timeout
        
    async def scrape_reviews(self, place_url, max_reviews=50):
        """
        Scrape Google Reviews from a place URL
        
        Args:
            place_url (str): Google Maps place URL
            max_reviews (int): Maximum number of reviews to scrape
            
        Returns:
            list: List of review dictionaries
        """
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions'
                ]
            )
            
            # Create context with realistic user agent
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            try:
                # Navigate to the page
                print(f"Navigating to: {place_url}")
                await page.goto(place_url, wait_until='networkidle', timeout=self.timeout)
                
                # Wait for reviews section to load
                await page.wait_for_selector('[data-review-id]', timeout=10000)
                
                # Click on "Reviews" tab if not already active
                try:
                    reviews_button = page.locator('button[data-value="Sort"]').first
                    if await reviews_button.is_visible():
                        await reviews_button.click()
                        await page.wait_for_timeout(2000)
                except:
                    print("Reviews tab not found or already active")
                
                # Scroll to load more reviews
                reviews = await self._scroll_and_collect_reviews(page, max_reviews)
                
                print(f"Successfully scraped {len(reviews)} reviews")
                return reviews
                
            except Exception as e:
                print(f"Error during scraping: {str(e)}")
                return []
                
            finally:
                await browser.close()
    
    async def _scroll_and_collect_reviews(self, page, max_reviews):
        """Scroll through reviews and collect data"""
        reviews = []
        last_review_count = 0
        no_new_reviews_count = 0
        
        while len(reviews) < max_reviews and no_new_reviews_count < 3:
            # Get current page HTML
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract reviews from current page
            current_reviews = self._extract_reviews_from_html(soup)
            
            # Add new reviews (avoid duplicates)
            existing_ids = {review['review_id'] for review in reviews}
            new_reviews = [r for r in current_reviews if r['review_id'] not in existing_ids]
            reviews.extend(new_reviews)
            
            print(f"Collected {len(reviews)} reviews so far...")
            
            # Check if we got new reviews
            if len(reviews) == last_review_count:
                no_new_reviews_count += 1
            else:
                no_new_reviews_count = 0
                last_review_count = len(reviews)
            
            # Scroll down to load more reviews
            try:
                # Find the scrollable reviews container
                scrollable_div = page.locator('[data-review-id]').first.locator('xpath=ancestor::div[contains(@class, "review") or contains(@style, "overflow")]').first
                await scrollable_div.scroll_into_view_if_needed()
                
                # Scroll down multiple times
                for _ in range(3):
                    await page.keyboard.press('End')
                    await page.wait_for_timeout(1000)
                    
                await page.wait_for_timeout(2000)
                
            except Exception as e:
                print(f"Scrolling error: {e}")
                break
        
        return reviews[:max_reviews]
    
    def _extract_reviews_from_html(self, soup):
        """Extract review data from BeautifulSoup object"""
        reviews = []
        
        # Find all review containers
        review_containers = soup.find_all('div', {'data-review-id': True})
        
        for container in review_containers:
            try:
                review_data = self._parse_single_review(container)
                if review_data:
                    reviews.append(review_data)
            except Exception as e:
                print(f"Error parsing review: {e}")
                continue
        
        return reviews
    
    def _parse_single_review(self, container):
        """Parse a single review container"""
        try:
            # Extract review ID
            review_id = container.get('data-review-id', '')
            
            # Extract author name
            author_element = container.find('div', class_='d4r55')
            author = author_element.text.strip() if author_element else 'Unknown'
            
            # Extract rating
            rating_element = container.find('span', {'role': 'img'})
            rating = 0
            if rating_element:
                aria_label = rating_element.get('aria-label', '')
                rating_match = re.search(r'(\d+)', aria_label)
                rating = int(rating_match.group(1)) if rating_match else 0
            
            # Extract review text
            review_text_element = container.find('span', class_='wiI7pd')
            review_text = review_text_element.text.strip() if review_text_element else ''
            
            # If review is truncated, try to find "More" button and full text
            if not review_text:
                # Try alternative selectors for review text
                alt_text_element = container.find('div', class_='MyEned')
                if alt_text_element:
                    review_text = alt_text_element.get_text(strip=True)
            
            # Extract date
            date_element = container.find('span', class_='rsqaWe')
            date = date_element.text.strip() if date_element else 'Unknown'
            
            # Extract author info (Local Guide status, review count, etc.)
            author_info_element = container.find('div', class_='RfnDt')
            author_info = author_info_element.text.strip() if author_info_element else ''
            
            # Extract photos count
            photo_elements = container.find_all('button', {'data-photo-index': True})
            photos_count = len(photo_elements)
            
            return {
                'review_id': review_id,
                'author': author,
                'author_info': author_info,
                'rating': rating,
                'date': date,
                'review_text': review_text,
                'photos_count': photos_count,
                'has_photos': photos_count > 0
            }
            
        except Exception as e:
            print(f"Error parsing single review: {e}")
            return None

# Usage example
async def main():
    # Example Google Maps place URL
    # Replace this with the actual place URL you want to scrape
    place_url = "https://www.google.com/maps/place/Seng+Leong+Engineering+Sdn+Bhd/@-6.2689926,106.8060391,15z/data=!4m6!3m5!1s0x31cdadfab1e24e3d:0x8bf3d80f0f4ec0bc!8m2!3d3.0120919!4d101.4661837!16s%2Fg%2F11kwj5y3v7?entry=ttu&g_ep=EgoyMDI1MDkxMC4wIKXMDSoASAFQAw%3D%3D"
    
    scraper = GoogleReviewsScraper(headless=False)  # Set to True for headless mode
    
    # Scrape reviews
    reviews = await scraper.scrape_reviews(place_url, max_reviews=50)
    
    # Print results
    print(f"\nScraped {len(reviews)} reviews:")
    print("-" * 50)
    
    for i, review in enumerate(reviews, 1):
        print(f"\n{i}. Author: {review['author']}")
        print(f"   Rating: {review['rating']}/5 stars")
        print(f"   Date: {review['date']}")
        print(f"   Author Info: {review['author_info']}")
        print(f"   Photos: {review['photos_count']}")
        print(f"   Review: {review['review_text'][:200]}{'...' if len(review['review_text']) > 200 else ''}")
    
    # Save to JSON file
    with open('google_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    
    print(f"\nReviews saved to 'google_reviews.json'")

# Alternative function for scraping from already loaded HTML
def scrape_from_html_file(html_file_path):
    """Scrape reviews from a saved HTML file"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    scraper = GoogleReviewsScraper()
    reviews = scraper._extract_reviews_from_html(soup)
    
    return reviews

if __name__ == "__main__":
    # Run the scraper
    asyncio.run(main())
    
    # Or scrape from HTML file:
    # reviews = scrape_from_html_file('reviews.html')
    # print(f"Found {len(reviews)} reviews in HTML file")