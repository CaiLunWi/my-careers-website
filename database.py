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

        
        
    
  