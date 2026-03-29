import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver  # Importing Selenium for JavaScript-heavy sites


class JobScraper:
    def __init__(self):
        self.job_titles = ['data analyst', 'data engineer', 'data scientist']
        self.date_filter = timedelta(days=2)

    def scrape_jobs(self, url):
        # Setup for Selenium
        driver = webdriver.Chrome()  # Initialize the Selenium WebDriver
        driver.get(url)  # Open the URL
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()  # Close the WebDriver

        jobs = []  # Initialize a list to collect job postings
        today = datetime.utcnow()

        # Example scraping logic (to be updated with actual HTML structure)
        for listing in soup.find_all('div', class_='job-listing'):
            title = listing.find('h2').get_text().lower()
            date_posted = self.extract_posted_date(listing.find('span', class_='date').get_text())

            if any(job_title in title for job_title in self.job_titles) and \
                (today - date_posted) <= self.date_filter:
                jobs.append(title)

        return jobs

    def extract_posted_date(self, date_string):
        # Example function to convert date_string to datetime object
        return datetime.strptime(date_string, '%Y-%m-%d')  # Adjust format as necessary

# Example usage:
if __name__ == '__main__':
    scraper = JobScraper()
    print(scraper.scrape_jobs('http://example.com/jobs'))
