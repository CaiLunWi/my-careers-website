from flask import Flask, render_template, jsonify, request, flash
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, register_user, load_users_from_db, get_user_by_id, get_user_by_username, load_coffee_from_db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

jobs = load_jobs_from_db()
users = load_users_from_db()
coffee = load_coffee_from_db()

class User(UserMixin):
  def __init__(self, user_id, username, email, user_role):
      self.id = user_id
      self.username = username
      self.email = email
      self.user_role = user_role

@login_manager.user_loader
def load_user(user_id):
  # Load user from the database based on user_id
  user_data = get_user_by_id(user_id)
  if user_data:
      return User(user_data['user_id'], user_data['username'], user_data['email'], user_data['user_role'])
  return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Validate user credentials
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = get_user_by_username(username)
        if user_data and user_data['password'] == password:
            user = User(user_data['user_id'], user_data['username'], user_data['email'], user_data['user_role'])
            login_user(user)
            flash('Login successful!', 'success')
            return render_template('dashboard.html', user=current_user)

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    print("Current User:", current_user)
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logout successful!', 'success')
  return render_template('login.html')

@app.route("/")
def hello_world():
  return render_template("home.html", jobs=jobs, company_name='Sangrai Kopi')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
  
@app.route('/career')
def career():
    return render_template('career.html', jobs=jobs)

@app.route('/coffee')
def coffee_page():
    return render_template('coffee.html', coffee=coffee)

@app.route("/api/job/<job_id>")
def show_job_json(job_id):
  job = load_job_from_db(job_id)
  return jsonify(job)

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
  add_application_to_db(job_id, data)
  return render_template('application_submitted.html', application=data, job=job)
  

@app.route('/register', methods=['post'])
def register_user_route():
  data = request.form
  register_user(data)
  return render_template('registration_success.html')
        


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)