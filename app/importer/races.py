import os
import csv
from collections import Counter

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import build_session, to_slug
from app.orm.race import RaceOrm
from app.orm.klass import KlassOrm

def races_importer():
  with build_session().begin() as session:
    races = set()
    races_to_classes = dict()

    klasses = session.execute(select(KlassOrm)).scalars().all()
    slug_to_klasses = { klass.slug: klass for klass in klasses }

    with open(os.path.join(ROOT_DIR, 'data', 'creatures.csv')) as csvfile:
      for row in csv.DictReader(csvfile):
        race = row.get("race", None)
        klass = row.get("klass", None)
        if race:
          races.add(race)
          if races_to_classes.get(race, None) is None:
            races_to_classes[race] = list()
          races_to_classes[race].append(klass)

    values = list()

    for race in races:
      klasses = races_to_classes[race]
      most_common_klass_slug = to_slug(max(klasses, key=Counter(klasses).get))
      most_common_klass = slug_to_klasses[most_common_klass_slug]

      value = { "name": race, "default_klass_id": most_common_klass.id, "slug": to_slug(race) }

      values.append(value)

    stmt = insert(RaceOrm).values(values)
    stmt = stmt.on_conflict_do_update(
      index_elements=["slug"],
      set_={
        "name": stmt.excluded.name,
        "description": stmt.excluded.description,
        "default_klass_id": stmt.excluded.default_klass_id,
      }
    )
    session.execute(stmt)