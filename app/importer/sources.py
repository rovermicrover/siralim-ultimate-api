import os
import csv

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import to_slug
from app.orm.base import Session
from app.orm.source import SourceOrm


def sources_importer():
    with Session.begin() as session:
        sources = set()

        with open(os.path.join(ROOT_DIR, "data", "creatures.csv")) as csvfile:
            for row in csv.DictReader(csvfile):
                sources.update(row["sources"].split(","))

        with open(os.path.join(ROOT_DIR, "data", "spells.csv")) as csvfile:
            for row in csv.DictReader(csvfile):
                sources.update(row["source"].split(","))

        values = [
            {"name": source, "slug": to_slug(source)} for source in sources
        ]

        # Uniq on slug
        values = list({value["slug"]: value for value in values}.values())

        stmt = insert(SourceOrm).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["slug"],
            set_={
                "name": stmt.excluded.name,
                "description": stmt.excluded.description,
                "updated_at": text("now()"),
            },
        )
        session.execute(stmt)
