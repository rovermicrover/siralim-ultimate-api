import os
import csv

from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import slug_default
from app.pg import build_session
from app.orm.klass import KlassOrm

def klasses_importer():
  with build_session().begin() as session:
    values = list()

    with open(os.path.join(ROOT_DIR, 'data', 'klasses.csv')) as csvfile:
      for row in csv.DictReader(csvfile):
        slug_default("name", row)
        values.append(row)

    stmt = insert(KlassOrm).values(values)
    stmt = stmt.on_conflict_do_update(
      index_elements=["slug"],
      set_={
        "name": stmt.excluded.name,
        "description": stmt.excluded.description,
        "color": stmt.excluded.color,
      }
    )
    session.execute(stmt)