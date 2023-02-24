from flask import Flask, render_template, jsonify
from database import load_jobs_from_db

app = Flask(__name__)

jobs = load_jobs_from_db()

@app.route("/")
def hello_world():
  return render_template("home.html", jobs=jobs, company_name='Sangrai Kopi')

@app.route("/api/jobs")
def list_jobs():
  return jsonify(jobs)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)