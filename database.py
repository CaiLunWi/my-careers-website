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
  with engine.connect() as con:
    result = con.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      row_as_dict = row._mapping
      jobs.append(dict(row_as_dict))
  return jobs
  