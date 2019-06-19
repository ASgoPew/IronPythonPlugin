import sys
import gc
import clr

sys.path.append('C:\Program Files\IronPython 2.7\Lib')
sys.path.append('C:\Program Files\IronPython 2.7\Lib\site-packages')

clr.AddReference('System.Core')
import System.Linq
clr.ImportExtensions(System.Linq)

import os
import time
import traceback
import clrtype
import json
from System.Threading.Tasks import Task
from System import *
from System.Collections.Generic import List

# Adds reference to already loaded in RAM assembly
# Meanwhile clr.AddReferenceToFileAndPath tries to load assembly even if it already was loaded in RAM
# so it loads uninitialized copy of assembly
#clr.AddReferenceByName("OTAPI")