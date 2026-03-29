import requests
from bs4 import BeautifulSoup
import time

class CareerPageScraper:
    def __init__(self, urls):
        self.urls = urls

    def scrape_career_pages(self):
        job_posts = []
        for url in self.urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            job_posts.extend(self.extract_jobs(soup))
            time.sleep(1)  # Respectful scraping to avoid getting blocked
        return job_posts

    def extract_jobs(self, soup):
        jobs = []
        for job in soup.find_all('div', class_='job-listing'):
            title = job.find('h2').text
            link = job.find('a')['href']
            jobs.append({'title': title, 'link': link})
        return jobs

if __name__ == '__main__':
    company_urls = [...]  # Replace with actual URLs
    scraper = CareerPageScraper(company_urls)
    jobs = scraper.scrape_career_pages()
    print(jobs)