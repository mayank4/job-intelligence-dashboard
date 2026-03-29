import requests
from bs4 import BeautifulSoup

def scrape_hacker_news_jobs():
    """Scrape Data/Analyst jobs from Hacker News Jobs board"""
    try:
        url = "https://news.ycombinator.com/jobs"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs = []
        job_rows = soup.find_all('tr', class_='athing')
        
        for row in job_rows[:30]:
            try:
                title_cell = row.find('span', class_='titleline')
                if not title_cell:
                    continue
                
                title_link = title_cell.find('a')
                if not title_link:
                    continue
                
                title = title_link.get_text(strip=True)
                job_url = title_link.get('href', '')
                
                # Filter for 'data' or 'analyst' keywords
                if 'data' not in title.lower() and 'analyst' not in title.lower():
                    continue
                
                # Get company and location from meta row
                meta_row = row.find_next('tr')
                company = "Unknown"
                location = "Remote"
                
                if meta_row:
                    meta_text = meta_row.get_text(strip=True)
                    parts = meta_text.split('|')
                    company = parts[0].strip() if len(parts) > 0 else "Unknown"
                    location = parts[1].strip() if len(parts) > 1 else "Remote"
                
                if not job_url.startswith('http'):
                    job_url = f"https://news.ycombinator.com/{job_url}"
                
                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'link': job_url,
                    'source': 'Hacker News'
                })
            except Exception as e:
                continue
        
        return jobs
    except Exception as e:
        print(f"Error scraping Hacker News: {e}")
        return []

def scrape_github_jobs():
    """Scrape Data/Analyst jobs from GitHub Jobs"""
    try:
        url = "https://jobs.github.com/positions.json?description=data"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        jobs_data = response.json()
        
        jobs = []
        for job in jobs_data[:20]:
            title = job.get('title', '')
            
            if 'data' not in title.lower() and 'analyst' not in title.lower():
                continue
            
            jobs.append({
                'title': title,
                'company': job.get('company', 'Unknown'),
                'location': job.get('location', 'Remote'),
                'link': job.get('url', ''),
                'source': 'GitHub Jobs'
            })
        
        return jobs
    except Exception as e:
        print(f"Error scraping GitHub Jobs: {e}")
        return []

def scrape_remoteok_jobs():
    """Scrape Data/Analyst jobs from RemoteOK"""
    try:
        url = "https://remoteok.io/remote-jobs.json"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        jobs_data = response.json()
        
        jobs = []
        for job in jobs_data[:50]:
            if isinstance(job, dict):
                title = job.get('title', '')
                
                if 'data' not in title.lower() and 'analyst' not in title.lower():
                    continue
                
                jobs.append({
                    'title': title,
                    'company': job.get('company', 'Unknown'),
                    'location': job.get('location', 'Remote'),
                    'link': job.get('url', ''),
                    'source': 'RemoteOK'
                })
        
        return jobs
    except Exception as e:
        print(f"Error scraping RemoteOK: {e}")
        return []

def get_all_jobs():
    """Combine jobs from all sources and remove duplicates"""
    print("Fetching jobs from multiple sources...")
    all_jobs = []
    
    print("  → Scraping Hacker News...")
    all_jobs.extend(scrape_hacker_news_jobs())
    
    print("  → Scraping GitHub Jobs...")
    all_jobs.extend(scrape_github_jobs())
    
    print("  → Scraping RemoteOK...")
    all_jobs.extend(scrape_remoteok_jobs())
    
    # Remove duplicates
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    print(f"Found {len(unique_jobs)} unique Data/Analyst jobs\n")
    return unique_jobs[:50]

if __name__ == "__main__":
    jobs = get_all_jobs()
    for job in jobs:
        print(f"✓ {job['title']}")
        print(f"  Company: {job['company']} | Location: {job['location']}\n")
