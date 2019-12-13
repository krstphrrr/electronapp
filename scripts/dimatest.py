import sys
from os.path import normpath, split, splitext, join, basename, isdir
from os import getcwd
from scripts.arcnah import arcno
from scripts.new_primarykeys import pk_add, gap_pk, pg_send, drop_one, bsne_pk
from datetime import datetime
import pandas as pd

str = sys.argv[1]
if isdir(str):
    print(f'{str} is a directory, congrats (not a DIMA tho\')')
elif splitext(str)[1]==".mdb":
    print("LET THERE BE DIMA")
else:
    print("have you tried choosing a dima?")

sys.stdout.flush()
