import requests
from bs4 import BeautifulSoup

def scrape_job_board(url):
    # Send a GET request to the job board
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find job postings (this will need to be customized based on the job board's HTML structure)
    jobs = []
    job_elements = soup.find_all('div', class_='job-listing')  # Example class name
    for job_element in job_elements:
        title = job_element.find('h2').text.strip()  # Example tag and class for job title
        company = job_element.find('h3').text.strip()  # Example tag and class for company name
        location = job_element.find('span', class_='location').text.strip()  # Example class for location
        jobs.append({
            'title': title,
            'company': company,
            'location': location
        })

    return jobs

if __name__ == "__main__":
    url = 'https://example-job-board.com'  # Replace with the actual job board URL
    job_listings = scrape_job_board(url)
    for job in job_listings:
        print(f"Title: {job['title']}, Company: {job['company']}, Location: {job['location']}")
