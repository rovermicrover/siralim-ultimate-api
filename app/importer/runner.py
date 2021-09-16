from .klasses import klasses_importer
from .races import races_importer
from .status_effects import status_effects_importer
from .sources import sources_importer
from .traits import traits_importer
from .spells import spells_importer
from .creatures import creatures_importer

def run():
  klasses_importer()
  races_importer()
  status_effects_importer()
  sources_importer()
  traits_importer()
  spells_importer()
  creatures_importer()