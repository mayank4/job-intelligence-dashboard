from flask import Flask, render_template, jsonify
from scraper import get_all_jobs
from datetime import datetime

app = Flask(__name__)

# Global cache
jobs_cache = []
last_update = None

def fetch_jobs():
    """Fetch live jobs from scraper"""
    global jobs_cache, last_update
    try:
        jobs_cache = get_all_jobs()
        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"✓ Loaded {len(jobs_cache)} jobs from live sources")
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        jobs_cache = []
    return jobs_cache

def extract_skills(jobs):
    """Extract skills mentioned in job titles"""
    skills = {
        "Data Analysis": 0,
        "Python": 0,
        "SQL": 0,
        "Excel": 0,
        "Tableau": 0,
        "Power BI": 0,
        "AWS": 0,
        "Machine Learning": 0,
        "Pandas": 0,
        "R": 0
    }
    
    for job in jobs:
        title = job.get('title', '').lower()
        
        if 'python' in title:
            skills["Python"] += 1
        if 'sql' in title:
            skills["SQL"] += 1
        if 'excel' in title:
            skills["Excel"] += 1
        if 'tableau' in title:
            skills["Tableau"] += 1
        if 'power bi' in title or 'powerbi' in title:
            skills["Power BI"] += 1
        if 'aws' in title:
            skills["AWS"] += 1
        if 'machine learning' in title or 'ml' in title:
            skills["Machine Learning"] += 1
        if 'pandas' in title:
            skills["Pandas"] += 1
        if 'data' in title or 'analyst' in title:
            skills["Data Analysis"] += 1
    
    # Remove zero values and return sorted
    return {k: v for k, v in sorted(skills.items(), key=lambda x: x[1], reverse=True) if v > 0}

@app.route("/")
def home():
    """Display dashboard with live jobs"""
    if not jobs_cache:
        fetch_jobs()
    
    skills = extract_skills(jobs_cache)
    return render_template("index.html", jobs=jobs_cache, skills=skills, last_update=last_update)

@app.route("/api/jobs")
def api_jobs():
    """Return live jobs as JSON"""
    if not jobs_cache:
        fetch_jobs()
    return jsonify(jobs_cache)

@app.route("/api/skills")
def api_skills():
    """Return extracted skills as JSON"""
    if not jobs_cache:
        fetch_jobs()
    skills = extract_skills(jobs_cache)
    return jsonify(skills)

@app.route("/api/refresh")
def refresh_jobs():
    """Manually refresh job listings"""
    jobs = fetch_jobs()
    return jsonify({
        "status": "success",
        "jobs_count": len(jobs),
        "last_update": last_update
    }), 200

@app.route("/health")
def health():
    """Health check"""
    return jsonify({"status": "ok", "jobs_cached": len(jobs_cache)}), 200

if __name__ == "__main__":
    print("Starting Job Intelligence Dashboard...")
    print("Initializing job data on startup...\n")
    fetch_jobs()
    app.run(debug=True, port=5000)
