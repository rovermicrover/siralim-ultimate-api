import os
import csv
from collections import Counter

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import slug_default, to_slug
from app.orm.base import Session
from app.orm.race import RaceOrm
from app.orm.klass import KlassOrm
from app.importer.icons import load_icon_to_base64

NEEDED_KEYS = [
    "name",
    "description",
    "icon",
    "default_klass",
]


RACE_ICONS_PATH = os.path.join(ROOT_DIR, "data", "race_icons")


def races_importer():
    with Session.begin() as session:
        values = []

        klasses = session.execute(select(KlassOrm)).scalars().all()
        slug_to_klasses = {klass.slug: klass for klass in klasses}

        with open(os.path.join(ROOT_DIR, "data", "races.csv")) as csvfile:
            for row in csv.DictReader(csvfile):
                value = {key: row[key] for key in NEEDED_KEYS}
                slug_default("name", value)

                icon = value.pop("icon")
                icon_file = os.path.join(RACE_ICONS_PATH, icon)
                value["icon"] = load_icon_to_base64(icon_file)

                default_klass = value.pop("default_klass")
                value["default_klass_id"] = slug_to_klasses[
                    to_slug(default_klass)
                ].id

                values.append(value)

        stmt = insert(RaceOrm).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["slug"],
            set_={
                "name": stmt.excluded.name,
                "description": stmt.excluded.description,
                "default_klass_id": stmt.excluded.default_klass_id,
                "icon": stmt.excluded.icon,
                "updated_at": text("now()"),
            },
        )
        session.execute(stmt)
