from flask import Flask, render_template, jsonify, redirect, url_for
from scraper import get_all_jobs
from datetime import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jobs_cache = []
last_update = None

def fetch_jobs():
    global jobs_cache, last_update
    try:
        jobs_cache = get_all_jobs()
        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Loaded {len(jobs_cache)} jobs")
        return jobs_cache
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        return []

@app.route("/")
def home():
    if not jobs_cache:
        fetch_jobs()
    return render_template("index.html", jobs=jobs_cache, last_update=last_update)

@app.route("/job/<int:job_id>")
def view_job(job_id):
    if 0 <= job_id < len(jobs_cache):
        return redirect(jobs_cache[job_id].get('link', '/'))
    return redirect("/")

@app.route("/api/jobs")
def api_jobs():
    if not jobs_cache:
        fetch_jobs()
    return jsonify(jobs_cache)

@app.route("/api/refresh")
def refresh_jobs():
    jobs = fetch_jobs()
    return jsonify({"status": "success", "count": len(jobs), "updated": last_update})

if __name__ == "__main__":
    fetch_jobs()
    app.run(debug=True, port=5000)