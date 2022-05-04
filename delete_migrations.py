import glob
import os
from os.path import join
from pathlib import Path

from APP import settings

for each in glob.glob(join(settings.BASE_DIR / '*' / 'migrations', "*.py")):
    if 'venv' in each:
        continue
    if '__init__.py' in each:
        continue
    print(each)
    os.remove(Path(each).resolve())
