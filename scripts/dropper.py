import sys, pyodbc, pandas as pd
from os import listdir,getcwd, chdir
from os.path import normpath, split, splitext, join, basename, isdir
from configparser import ConfigParser
from psycopg2 import connect, sql
from psycopg2.pool import SimpleConnectionPool
from sqlalchemy import create_engine
from datetime import datetime
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


def config(filename='./scripts/database.ini', section='dima'):
    """
    Uses the configpaser module to read .ini and return a dictionary of
    credentials
    """
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(
        section, filename))

    return db


class db:
    params = config()
    # str = connect(**params)
    tmpconstr = SimpleConnectionPool(minconn=1,maxconn=5,**params)
    str= tmpconstr.getconn()

    def __init__(self):
        params = config()
        self._conn = connect(**params)
        self._cur= self._conn.cursor()

def drop_one(table):
    con = db.str
    cur = db.str.cursor()
    try:
        cur.execute(
        sql.SQL('DROP TABLE IF EXISTS postgres.public.{0}').format(
                 sql.Identifier(table))
    )
        con.commit()
        print(f'successfully dropped {table}')


    except Exception as e:
        print(e)
try:
    for table in maintablelist:
        drop_one(table)
    for table in newtables:
        drop_one(table)
    print("dropped tables in postgres")
except Exception as e:
    print(e)
# print(str)
