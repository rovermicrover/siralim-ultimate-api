from app.importer.traits import NEEDED_KEYS
import os
import csv
import base64

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import slug_default, to_slug
from app.orm.base import Session
from app.orm.status_effect import StatusEffectOrm

NEEDED_KEYS = [
    "name",
    "description",
    "category",
    "turns",
    "leave_chance",
    "max_stacks",
    "icon",
]
STATUS_ICONS_PATH = os.path.join(ROOT_DIR, "data", "status_icons")


def status_effects_importer():
    with Session.begin() as session:
        values = list()

        with open(
            os.path.join(ROOT_DIR, "data", "status_effects.csv")
        ) as csvfile:
            for row in csv.DictReader(csvfile):
                value = {key: row[key] for key in NEEDED_KEYS}
                slug_default("name", value)

                if not value["turns"]:
                    value["turns"] = None

                if not value["leave_chance"]:
                    value["leave_chance"] = None

                icon = value.pop("icon")
                icon_file = os.path.join(STATUS_ICONS_PATH, icon)
                icon_base64 = base64.b64encode(
                    open(icon_file, "rb").read()
                ).decode("utf-8")
                value["icon"] = f"data:image/png;base64,{icon_base64}"

                values.append(value)

        stmt = insert(StatusEffectOrm).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["slug"],
            set_={
                "name": stmt.excluded.name,
                "description": stmt.excluded.description,
                "category": stmt.excluded.category,
                "turns": stmt.excluded.turns,
                "leave_chance": stmt.excluded.leave_chance,
                "max_stacks": stmt.excluded.max_stacks,
                "icon": stmt.excluded.icon,
            },
        )
        session.execute(stmt)
