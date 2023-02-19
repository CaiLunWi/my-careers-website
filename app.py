from flask import Flask, render_template

app = Flask(__name__)


JOBS = [
  {
    'job_id': 1,
    'title': 'Barista',
    'location': 'Indonesia, Jakarta',
    'salary': '4000 yuan'
  },
  {
    'job_id': 2,
    'title': 'Cafeteria Cook',
    'location': 'Indonesia, Jakarta',
    'salary': '3800 yuan'
  },
  {
    'job_id': 3,
    'title': 'Cafeteria Worker',
    'location': 'Indonesia, Jakarta',
    'salary': '3500 yuan'
  },
  {
    'job_id': 4,
    'title': 'Cafe Attendant',
    'location': 'Indonesia, Jakarta',
  }
]

@app.route("/")
def hello_world():
  return render_template("home.html", jobs=JOBS, company_name='Sangrai Kopi')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)