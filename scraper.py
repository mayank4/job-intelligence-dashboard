# scraper.py - FIXED VERSION

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from job_sources import COMPANY_CAREER_PAGES, KEYWORDS, DATE_FILTER_DAYS

class JobScraper:
    def __init__(self):
        self.keywords = KEYWORDS
        self.date_filter = timedelta(days=DATE_FILTER_DAYS)

    def scrape_career_page(self, url, company):
        """Scrape a single career page"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            jobs = []
            # Look for common job listing patterns
            for job_elem in soup.find_all(['div', 'li'], class_=['job', 'position', 'job-card']):
                try:
                    title_elem = job_elem.find(['h2', 'h3', 'a'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True).lower()
                    
                    # Check if job matches keywords
                    if not any(keyword.lower() in title for keyword in self.keywords):
                        continue
                    
                    link_elem = job_elem.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    
                    if link and not link.startswith('http'):
                        link = url.rstrip('/') + '/' + link.lstrip('/')
                    
                    jobs.append({
                        'title': title_elem.get_text(strip=True),
                        'company': company,
                        'link': link,
                        'source': 'Career Page',
                        'location': 'Remote/On-site'
                    })
                except:
                    continue
            
            return jobs
        except Exception as e:
            print(f"Error scraping {company}: {e}")
            return []

    def scrape_all_sources(self):
        """Scrape all company career pages"""
        all_jobs = []
        print("\n🚀 Scraping job listings...\n")
        
        for company, url in COMPANY_CAREER_PAGES.items():
            print(f"  → {company}")
            jobs = self.scrape_career_page(url, company)
            all_jobs.extend(jobs)
        
        # Remove duplicates
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        print(f"\n✅ Found {len(unique_jobs)} jobs\n")
        return unique_jobs

def get_all_jobs():
    """Main function - returns all jobs"""
    scraper = JobScraper()
    return scraper.scrape_all_sources()

if __name__ == "__main__":
    jobs = get_all_jobs()
    for job in jobs[:5]:
        print(f"✓ {job['title']} - {job['company']}")
