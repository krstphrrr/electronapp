import sys
from os.path import normpath, split, splitext, join, basename, isdir
from os import getcwd
from scripts.arcnah import arcno
from scripts.new_primarykeys import pk_add, gap_pk, pg_send, drop_one, bsne_pk
from datetime import datetime
import pandas as pd
"""
loop successfully adds all columns to chosen tables, and ingests it.
if table already exists, it appends it to existing table in db.
"""



str = sys.argv[1]
# string = r"C:\Users\kbonefont\Desktop\JER DDT DIMA 5.3b as of 2018-10-23.mdb"
# splitext(basename(string))[0]


maintablelist = ['tblPlots',
  'tblLines',
  'tblLPIDetail',
  'tblLPIHeader',
  'tblGapDetail',
  'tblGapHeader',
  'tblQualHeader',
  'tblQualDetail',
  'tblSoilStabHeader',
  'tblSoilStabDetail',
  'tblSoilPitHorizons',
  'tblSoilPits',
  'tblSpecRichHeader',
  'tblSpecRichDetail',
  'tblPlantProdHeader',
  'tblPlantProdDetail',
  'tblPlotNotes',
  'tblPlantDenHeader',
  'tblPlantDenDetail',
  'tblSpecies',
  'tblSpeciesGeneric',
  'tblSites',
  'tblBSNE_Box',
  'tblBSNE_Stack',
  'tblBSNE_TrapCollection']

if isdir(str):
    # for table in maintablelist:
        # pg_send(f'{table}',str)
        # print(f'dima "{splitext(basename(str))[0]}" was uploaded!')
    print(f'dima "{splitext(basename(str))[0]}" was uploaded!')
else:
    print('yeah, you need to choose a dima, bud.')
sys.stdout.flush()
