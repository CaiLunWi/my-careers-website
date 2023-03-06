from sqlalchemy import create_engine, text, bindparam
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
    
    

        
        
    
  