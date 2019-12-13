from os.path import normpath, split, splitext, join
from arcnah import arcno
from new_primarykeys import pk_add, gap_pk, pg_send, drop_one, bsne_pk
from datetime import datetime
import pandas as pd
"""
loop successfully adds all columns to chosen tables, and ingests it.
if table already exists, it appends it to existing table in db.
to-do:
- figure out ddt data
- deal with extra columns:
- maybe creating on-the-fly table schemas and bulk upload?
"""

str = sys.argv[1]

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

 newtables = [
  'tblHorizontalFlux',
  'tblHorizontalFlux_Locations',
  'tblDustDeposition',
  'tblDustDeposition_Locations'
  ]

for table in maintablelist:
    drop_one(table)
# dropping all tables
for table in newtables:
    drop_one(table)
