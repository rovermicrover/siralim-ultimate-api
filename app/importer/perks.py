import os
import csv
from collections import Counter

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import slug_default, to_slug
from app.orm.base import Session
from app.orm.perk import PerkOrm
from app.orm.specialization import SpecializationOrm
from app.importer.icons import load_icon_to_base64
from .tags import get_tag_regexes, get_tags

NEEDED_KEYS = [
    "name",
    "description",
    "specialization",
    "ranks",
    "cost",
    "ascension",
    "annointment",
]


RACE_ICONS_PATH = os.path.join(ROOT_DIR, "data", "race_icons")


def perks_importer():
    with Session.begin() as session:
        tag_regexes = get_tag_regexes(session)
        values = []

        specializations = (
            session.execute(select(SpecializationOrm)).scalars().all()
        )
        slug_to_specializations = {
            specialization.slug: specialization
            for specialization in specializations
        }

        with open(os.path.join(ROOT_DIR, "data", "perks.csv")) as csvfile:
            for row in csv.DictReader(csvfile):
                value = {key: row[key] for key in NEEDED_KEYS}
                slug_default("name", value)

                specialization = value.pop("specialization")
                value["specialization_id"] = slug_to_specializations[
                    to_slug(specialization)
                ].id

                value["ascension"] = value["ascension"].lower() == "yes"
                value["annointment"] = value["annointment"].lower() == "yes"

                value["tags"] = get_tags(tag_regexes, value["description"])

                values.append(value)

        stmt = insert(PerkOrm).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["slug"],
            set_={
                "name": stmt.excluded.name,
                "description": stmt.excluded.description,
                "specialization_id": stmt.excluded.specialization_id,
                "ranks": stmt.excluded.ranks,
                "cost": stmt.excluded.cost,
                "ascension": stmt.excluded.ascension,
                "annointment": stmt.excluded.annointment,
                "tags": stmt.excluded.tags,
                "updated_at": text("now()"),
            },
        )
        session.execute(stmt)
