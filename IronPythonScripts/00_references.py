import sys
import gc
import clr

clr.AddReference('System.Core')
import System.Linq
clr.ImportExtensions(System.Linq)

import os
import time
import traceback
#import clrtype
#import json
import random

from System import *
from System.Collections.Generic import List
from System.Threading.Tasks import Task
from System.Threading import Monitor, Thread
from System.IO import Path
from System.Timers import Timer

# Adds reference to already loaded in RAM assembly
# Meanwhile clr.AddReferenceToFileAndPath tries to load assembly even if it already was loaded in RAM
# so it loads uninitialized copy of assembly.
#	clr.AddReferenceByName("OTAPI")

# You can import extensions defined in a class:
#	import SomeClass
#	clr.ImportExtensions(SomeClass)

global loaded
loaded = False
