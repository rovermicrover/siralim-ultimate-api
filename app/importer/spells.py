import os
import csv
from collections import Counter

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import slug_default, to_slug
from app.orm.base import Session
from app.orm.spell import SpellOrm
from app.orm.klass import KlassOrm
from app.orm.source import SourceOrm
from .tags import get_tag_regexes, get_tags

NEEDED_KEYS = {"name", "klass", "charges", "source", "description"}


def spells_importer():
    with Session.begin() as session:
        tag_regexes = get_tag_regexes(session)
        values = list()

        klasses = session.execute(select(KlassOrm)).scalars().all()
        slug_to_klasses = {klass.slug: klass for klass in klasses}

        sources = session.execute(select(SourceOrm)).scalars().all()
        slug_to_sources = {source.slug: source for source in sources}

        with open(os.path.join(ROOT_DIR, "data", "spells.csv")) as csvfile:
            for row in csv.DictReader(csvfile):
                value = {key: row[key] for key in NEEDED_KEYS}
                slug_default("name", value)

                klass = value.pop("klass")
                source = value.pop("source")

                value["klass_id"] = slug_to_klasses[to_slug(klass)].id
                value["source_id"] = slug_to_sources[to_slug(source)].id

                value["tags"] = get_tags(tag_regexes, value["description"])

                values.append(value)

        stmt = insert(SpellOrm).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["slug"],
            set_={
                "name": stmt.excluded.name,
                "description": stmt.excluded.description,
                "klass_id": stmt.excluded.klass_id,
                "source_id": stmt.excluded.source_id,
                "tags": stmt.excluded.tags,
            },
        )
        session.execute(stmt)
