from sqlalchemy import create_engine, text
import os

connection_string = os.environ['CONNECTION_STRING']

engine = create_engine(
  connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all():
            row_as_dict = row._mapping
            jobs.append(dict(row_as_dict))
    return jobs

def load_users_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from users"))
        users = []
        for row in result.all():
            row_as_dict = row._mapping
            users.append(dict(row_as_dict))
    return users


def load_job_from_db(job_id):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM jobs WHERE job_id = :job_id"),         
    dict(job_id=job_id))
    rows = result.all() 
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0]._mapping)

def add_application_to_db(id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES(:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")
    job_id=id,
    full_name=data['full_name'],
    email=data['email'],
    linkedin_url=data['linkedin_url'],
    education=data['education'],
    work_experience=data['work_experience'],
    resume_url=data['resume_url']
    conn.execute(query,
                 [
                   {"job_id": job_id, "full_name": full_name, "email": email, "linkedin_url": linkedin_url, "education": education, "work_experience": work_experience, "resume_url": resume_url}
                 ])

def register_user(data):
  with engine.connect() as conn:
      # Insert the user information into the Users table
      query = text("INSERT INTO users (username, email, password, user_role) VALUES (:username, :email, :password, :user_role)")
      username = data['username']
      email = data['email']
      password = data['password']
      user_role = '0'
      conn.execute(query,
                   [
                       {"username": username, "email": email, "password": password, "user_role": user_role}
                   ])

def get_user_by_id(user_id):
  with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM users WHERE user_id =         :user_id"), dict(user_id=user_id))
      rows = result.all() 
      if len(rows) == 0:
        return None
      else:
        return dict(rows[0]._mapping)

def get_user_by_username(username):
  with engine.connect() as conn:
      result = conn.execute(
      text("SELECT * FROM users WHERE username = :username"),       
      dict(username=username))
      rows = result.all() 
      if len(rows) == 0:
        return None
      else:
        return dict(rows[0]._mapping)

def load_coffee_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from coffee"))
    coffee = []
    for row in result.all():
        row_as_dict = row._mapping
        coffee.append(dict(row_as_dict))
    return coffee
    

        
        
    
  