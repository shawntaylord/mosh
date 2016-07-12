import os
from mosh.constants import *

def cd(args):
  os.chdir(args[0])

  return STATUS_RUN
