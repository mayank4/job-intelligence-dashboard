from datetime import datetime, timedelta
import re


def parse_job_date(date_str):
    """Parses job posting date from a given string."""
    date_patterns = {
        'iso': r'\d{4}-\d{2}-\d{2}',  # Pattern for ISO Dates
        'relative': r'\d+\s+(days?|hours?)\s+ago'
    }

    for pattern in date_patterns.values():
        match = re.search(pattern, date_str)
        if match:
            if 'iso' in pattern:
                return datetime.fromisoformat(match.group())  # Assuming ISO format
            else:
                return datetime.utcnow() - timedelta(days=int(match.group(1)))
    return None  # If no pattern matched


def is_recent_job(posted_date):
    """Checks if a job was posted in the last 1-2 days."""
    now = datetime.utcnow()
    recent_threshold = now - timedelta(days=2)
    return posted_date >= recent_threshold


def parse_iso_date(date_str):
    """Parses an ISO formatted date string."""
    return datetime.fromisoformat(date_str)


def get_jobs_within_days(jobs, days=2):
    """Filters a list of jobs to include only those posted within the last specified number of days."""
    recent_jobs = []
    now = datetime.utcnow()
    threshold = now - timedelta(days=days)
    for job in jobs:
        posted_date = parse_job_date(job['date_posted'])
        if posted_date and posted_date >= threshold:
            recent_jobs.append(job)
    return recent_jobs
