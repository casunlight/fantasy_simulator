import os
import sys


print('testing2 __name__: '+str(__name__))
print('testing2 cd: '+str(os.curdir))
print('testing2 cwd: '+str(os.getcwd()))

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

