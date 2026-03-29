from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    skills = {"Python": 45, "SQL": 42, "Excel": 38, "Tableau": 32, "Power BI": 28}
    jobs = [{"title": "Python Developer", "company": "Google", "location": "Mountain View", "link": "https://google.com/jobs/1"}]
    return render_template("index.html", skills=skills, jobs=jobs)

@app.route("/api/skills")
def api_skills():
    return jsonify({"Python": 45, "SQL": 42})

@app.route("/api/jobs")
def api_jobs():
    return jsonify([{"title": "Python Developer"}])

if __name__ == "__main__":
    app.run(debug=True, port=5000)