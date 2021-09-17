from enum import Enum


class StatusEffectCategoriesEnum(str, Enum):
    buff = "buff"
    debuff = "debuff"
    minion = "minion"
