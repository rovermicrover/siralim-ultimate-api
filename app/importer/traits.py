import os
import csv

from collections import Counter
from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import build_session, slug_default
from app.orm.trait import TraitOrm

NEEDED_KEYS = { "name", "material_name", "description" }

def traits_importer():
  with build_session().begin() as session:
    values = list()

    with open(os.path.join(ROOT_DIR, 'data', 'traits.csv')) as csvfile:
      for row in csv.DictReader(csvfile):
        value = { key: row[key] for key in NEEDED_KEYS }
        slug_default("name", value)

        if value["material_name"].lower() == "n/a":
          value["material_name"] = None

        values.append(value)

    stmt = insert(TraitOrm).values(values)
    stmt = stmt.on_conflict_do_update(
      index_elements=["slug"],
      set_={
        "name": stmt.excluded.name,
        "description": stmt.excluded.description,
        "material_name": stmt.excluded.material_name,
      }
    )
    session.execute(stmt)