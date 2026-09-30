# Lets the tests import runner, checker and levels from the project folder.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
