import os
import csv

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from app.config import ROOT_DIR
from app.orm.base import slug_default
from app.orm.base import Session
from app.orm.specialization import SpecializationOrm
from .icons import load_icon_to_base64

SPECS_ICONS_PATH = os.path.join(ROOT_DIR, "data", "specialization_icons")


def specializations_importer():
    with Session.begin() as session:
        values = list()

        with open(
            os.path.join(ROOT_DIR, "data", "specializations.csv")
        ) as csvfile:
            for row in csv.DictReader(csvfile):
                value = row.copy()
                slug_default("name", value)

                icon = value.pop("icon")
                icon_file = os.path.join(SPECS_ICONS_PATH, icon)
                value["icon"] = load_icon_to_base64(icon_file)

                values.append(value)

        stmt = insert(SpecializationOrm).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["slug"],
            set_={
                "name": stmt.excluded.name,
                "description": stmt.excluded.description,
                "icon": stmt.excluded.icon,
                "updated_at": text("now()"),
            },
        )
        session.execute(stmt)
