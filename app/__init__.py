import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(
    create_engine(os.environ["DATABASE_URL"], echo=True, future=True)
)
