from typing import List
import re
from functools import reduce

from sqlalchemy import select
from app.orm.base import Session

from app.orm.klass import KlassOrm
from app.orm.race import RaceOrm
from app.orm.status_effect import StatusEffectOrm


def get_tag_regexes(session):
    klasses = session.execute(select(KlassOrm)).scalars().all()
    races = session.execute(select(RaceOrm)).scalars().all()
    status_effects = session.execute(select(StatusEffectOrm)).scalars().all()

    tag_regexes = {
        "does-not-stack": [
            re.compile("This trait does not stack", re.IGNORECASE)
        ],
        "cast": [re.compile(r"\bCast[s]?\b")],
        "attacks": [re.compile(r"\bAttacks\b")],
        "attacked": [re.compile(r"\bAttacked\b")],
        "provoke": [re.compile(r"\bProvok(es)?(ing)?\b")],
        "defend": [re.compile(r"\bDefend(s)?(ing)?\b")],
        "spell-gem": [re.compile(r"\bSpell Gem(s)?\b")],
        "timeline": [re.compile(r"\bTimeline\b")],
        "health": [re.compile(r"\bHealth\b")],
        "current-health": [re.compile(r"\bCurrent Health\b")],
        "maximum-health": [re.compile(r"\bMaximum Health\b")],
        "attack": [re.compile(r"\bAttack\b")],
        "intelligence": [re.compile(r"\bIntelligence\b")],
        "defense": [re.compile(r"\bDefense\b")],
        "speed": [re.compile(r"\bSpeed\b")],
        "buff": [re.compile(r"\bbuff(s)?\b", re.IGNORECASE)],
        "debuff": [re.compile(r"\bdebuff(s)?\b", re.IGNORECASE)],
        "minion": [re.compile(r"\bminion(s)?\b", re.IGNORECASE)],
        "race": [re.compile(r"\brace(s)?\b", re.IGNORECASE)],
        "class": [re.compile(r"\bclass(es)?\b", re.IGNORECASE)],
        "resurrect": [re.compile(r"\bresurrect(ion)?(ed)?\b", re.IGNORECASE)],
        "heal": [re.compile(r"\bheal(ing)?(ed)?\b", re.IGNORECASE)],
        "turns-taken": [
            re.compile(
                r"\\bfor each turn they've taken in the current battle\b",
                re.IGNORECASE,
            )
        ],
        "dodge": [re.compile(r"\bdodge(s)?(ed)?\b", re.IGNORECASE)],
        "critical": [re.compile(r"\bcritical\b", re.IGNORECASE)],
    }

    for k in klasses:
        tag = f"class-{k.slug}"
        regex_string = r"\b" + re.escape(k.name) + r"\b"
        tag_regexes[tag] = [re.compile(regex_string)]
        tag_regexes["class"].append(re.compile(regex_string))

    for r in races:
        tag = f"race-{r.slug}"
        regex_string = r"\b" + re.escape(r.name) + r"\b"
        tag_regexes[tag] = [re.compile(regex_string)]
        tag_regexes["race"].append(re.compile(regex_string))

    for se in status_effects:
        tag = f"{se.category}-{se.slug}"
        regex_string = r"\b" + re.escape(se.name) + r"\b"
        tag_regexes[tag] = [re.compile(regex_string)]
        tag_regexes[se.category].append(re.compile(regex_string))

    return tag_regexes


def get_tags(tag_regexes, text: str):
    def reduce_tags(memo: List[str], tag_regexes):
        tag, regexes = tag_regexes
        if any(r.search(text) for r in regexes):
            memo.append(tag)
        return memo

    return reduce(reduce_tags, tag_regexes.items(), [])
