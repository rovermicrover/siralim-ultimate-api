import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def build_session():
  return sessionmaker(create_engine(os.environ['DATABASE_URL'], echo=True, future=True))