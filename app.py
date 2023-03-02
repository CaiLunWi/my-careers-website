from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db

app = Flask(__name__)

jobs = load_jobs_from_db()

@app.route("/")
def hello_world():
  return render_template("home.html", jobs=jobs, company_name='Sangrai Kopi')

@app.route("/api/jobs")
def list_jobs():
  return jsonify(jobs)

@app.route("/jobs/<job_id>")
def show_job(job_id):
  job = load_job_from_db(job_id)
  if not job:
    return "Not Found"
  return render_template("jobpage.html", job=job)

@app.route("/jobs/<job_id>/apply", methods=['post'])
def apply_for_job(job_id):
  data = request.form
  job = load_job_from_db(job_id)
  # store this in DB
  # send an email
  return render_template('application_submitted.html', application=data, job=job)
  


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)