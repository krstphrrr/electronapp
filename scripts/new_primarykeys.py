from arcnah import arcno
from os.path import normpath, split, splitext, join
from utils import db
from sqlalchemy import create_engine
from utils import sql_str, config
from datetime import datetime
from psycopg2 import sql
import pandas as pd
"""
None-BSNE data: 'PlotKey' + 'FormDate' on most atomic level
BSNE data: 'PlotKey' + 'collectDate'

to-do:
- refactor all

"""


"""
creating dataframes that create a primary key at most atomic level And
propagate it outward:
1. LPI
2. Gap
3. SpeRick
4. PlantDen
5. BSNE
"""


def lpi_pk(dimapath):
    # tables
    arc = arcno()
    lpi_header = arc.MakeTableView('tblLPIHeader', dimapath)
    lpi_detail = arc.MakeTableView('tblLPIDetail', dimapath)
    lines = arc.MakeTableView('tblLines', dimapath)
    plots = arc.MakeTableView('tblPlots', dimapath)
    # joins
    plot_line = arc.AddJoin(plots,lines, 'PlotKey','PlotKey')
    lpihead_detail = arc.AddJoin(lpi_header, lpi_detail, 'RecKey')
    plot_line_det = arc.AddJoin(plot_line, lpihead_detail, 'LineKey', 'LineKey')

    plot_pk = arc.CalculateField(plot_line_det, "PrimaryKey", "PlotKey", "FormDate")

    return plot_pk

def gap_pk(dimapath):
    # tables
    arc = arcno()
    gap_header = arc.MakeTableView('tblGapHeader', dimapath)
    gap_detail = arc.MakeTableView('tblGapDetail', dimapath)
    lines = arc.MakeTableView('tblLines', dimapath)
    plots = arc.MakeTableView('tblPlots', dimapath)
    # joins
    plot_line = arc.AddJoin(plots,lines, 'PlotKey','PlotKey')
    gaphead_detail = arc.AddJoin(gap_header, gap_detail, 'RecKey')
    plot_line_det = arc.AddJoin(plot_line, gaphead_detail, 'LineKey', 'LineKey')

    plot_pk = arc.CalculateField(plot_line_det, "PrimaryKey", "PlotKey", "FormDate")

    return plot_pk

def sperich_pk(dimapath):
    # tables
    arc = arcno()
    spe_header = arc.MakeTableView('tblSpecRichHeader', dimapath)
    spe_detail = arc.MakeTableView('tblSpecRichDetail', dimapath)
    lines = arc.MakeTableView('tblLines', dimapath)
    plots = arc.MakeTableView('tblPlots', dimapath)
    # joins
    plot_line = arc.AddJoin(plots,lines, 'PlotKey','PlotKey')
    spehead_detail = arc.AddJoin(spe_header, spe_detail, 'RecKey')
    plot_line_det = arc.AddJoin(plot_line, spehead_detail, 'LineKey', 'LineKey')

    plot_pk = arc.CalculateField(plot_line_det, "PrimaryKey", "PlotKey", "FormDate")

    return plot_pk

def plantden_pk(dimapath):
    # tables
    arc = arcno()
    pla_header = arc.MakeTableView('tblPlantDenHeader', dimapath)
    pla_detail = arc.MakeTableView('tblPlantDenDetail', dimapath)
    lines = arc.MakeTableView('tblLines', dimapath)
    plots = arc.MakeTableView('tblPlots', dimapath)
    # joins
    plot_line = arc.AddJoin(plots,lines, 'PlotKey','PlotKey')
    plahead_detail = arc.AddJoin(pla_header, pla_detail, 'RecKey')
    plot_line_det = arc.AddJoin(plot_line, plahead_detail, 'LineKey', 'LineKey')

    plot_pk = arc.CalculateField(plot_line_det, "PrimaryKey", "PlotKey", "FormDate")

    return plot_pk

def bsne_pk(dimapath):
    ddt = arc.MakeTableView("tblBSNE_TrapCollection",dimapath)
    if ddt.shape[0]>0:
        ddt = arc.MakeTableView("tblBSNE_TrapCollection",dimapath)

        stack = arc.MakeTableView("tblBSNE_Stack", dimapath)

        df = arc.AddJoin(stack, ddt, "StackID", "StackID")
        # PlotKey+CollecDate
        df2 = arc.CalculateField(df,"PrimaryKey","PlotKey","collectDate")
        return df2
    else:

        box = arc.MakeTableView("tblBSNE_Box",dimapath)

        stack = arc.MakeTableView("tblBSNE_Stack", dimapath)
        boxcol = arc.MakeTableView('tblBSNE_BoxCollection', dimapath)

        df = arc.AddJoin(stack, box, "StackID", "StackID")
        df2 = arc.AddJoin(df,boxcol, "BoxID")
        df2 = arc.CalculateField(df2,"PrimaryKey","PlotKey","collectDate")
        return df2




"""
takes a dima tablename string and a dima path,
returns the table with the proper PrimaryKey field appended.
(works for the most part, depends on dima)
to-do:
- DONE implement sites table
- DONE detect calibration in dimapath and append to dbkey? or source
- DONE keep unexpected columns
- DONE new names for BSNE data: tblHorizontalFlux + locations, tblDustDeposition + locations
- DONE corresponding primarykey on new tables: location + collect date + plotkey

"""
arc = arcno()



def pk_add(tablename,dimapath):
    """
    adds primary key to the chosen table
    1. PlotKey pipe
    2. LineKey pipe
    3. reckey pipe
    4. pipe if its none of the above: only BSNE implemented
    """
    plot = None


    plotkeylist = ['tblPlots','tblLines','tblQualHeader','tblSoilStabHeader',
    'tblSoilPits','tblPlantProdHeader','tblPlotNotes', 'tblSoilPitHorizons']

    linekeylist = ['tblGapHeader','tblLPIHeader','tblSpecRichHeader',
    'tblPlantDenHeader']

    reckeylist = ['tblGapDetail','tblLPIDetail','tblQualDetail','tblSoilStabDetail',
    'tblSpecRichDetail','tblPlantProdDetail','tblPlantDenDetail']

    nonline = {'tblQualDetail':'tblQualHeader',
    'tblSoilStabDetail':'tblSoilStabHeader','tblPlantProdDetail':'tblPlantProdHeader'}

    arc = arcno()
    if tablename in plotkeylist:

        if tablename.find('Horizon')!=-1:
            fulldf = gap_pk(dimapath)
            if fulldf.shape[0]<1:
                fulldf = lpi_pk(dimapath)
            arc.isolateFields(fulldf, 'PlotKey','PrimaryKey')
            soil_tmp = arc.isolates
            plt = soil_tmp.rename(columns={'PlotKey':'PlotKey2'}).copy(deep=True)
            plt = plt.drop_duplicates(['PlotKey2'])
            plottable = arc.MakeTableView('tblSoilPits',dimapath)
            soil_pk = plt.merge(plottable, left_on=plt.PlotKey2, right_on=plottable.PlotKey)
            soil_pk.drop('PlotKey2', axis=1, inplace=True)
            soil_pk = soil_pk.copy(deep=True)
            soil_pk.drop('key_0', axis=1, inplace=True)
            hordf = arc.MakeTableView(f'{tablename}', dimapath)

            arc.isolateFields(soil_pk,'SoilKey','PrimaryKey')
            sk_tmp = arc.isolates
            plt = sk_tmp.rename(columns={'SoilKey':'SoilKey2'}).copy(deep=True)
            plt = plt.drop_duplicates(['SoilKey2'])
            soil_pk = plt.merge(hordf, left_on=plt.SoilKey2, right_on=hordf.SoilKey)
            soil_pk.drop('SoilKey2', axis=1, inplace=True)
            soil_pk = soil_pk.copy(deep=True)
            soil_pk.drop('key_0', axis=1, inplace=True)

            return soil_pk

        else:
            fulldf = gap_pk(dimapath)
            arc.isolateFields(fulldf, 'PlotKey','PrimaryKey')
            plot_tmp = arc.isolates
            plt = plot_tmp.rename(columns={'PlotKey':'PlotKey2'}).copy(deep=True)
            plt = plt.drop_duplicates(['PlotKey2'])
            plottable = arc.MakeTableView(f'{tablename}',dimapath)
            plot_pk = plt.merge(plottable, left_on=plt.PlotKey2, right_on=plottable.PlotKey)
            plot_pk.drop('PlotKey2', axis=1, inplace=True)
            plot_pk = plot_pk.copy(deep=True)
            plot_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] =plot_pk
            return plot_pk

    elif tablename in linekeylist:
        if tablename.find('Gap')!=-1:
            fulldf = gap_pk(dimapath)
            arc.isolateFields(fulldf, 'LineKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'LineKey':'LineKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['LineKey2'])
            linekeytable = arc.MakeTableView(f'{tablename}',dimapath)
            linekeytable_pk = lin.merge(linekeytable, left_on=lin.LineKey2, right_on=linekeytable.LineKey)
            linekeytable_pk.drop('LineKey2', axis=1, inplace=True)
            linekeytabler_pk = linekeytable_pk.copy(deep=True)
            linekeytable_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] = linekeytable_pk
            return linekeytable_pk

        elif tablename.find('LPI')!=-1:
            fulldf = lpi_pk(dimapath)
            arc.isolateFields(fulldf, 'LineKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'LineKey':'LineKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['LineKey2'])
            linekeytable = arc.MakeTableView(f'{tablename}',dimapath)
            linekeytable_pk = lin.merge(linekeytable, left_on=lin.LineKey2, right_on=linekeytable.LineKey)
            linekeytable_pk.drop('LineKey2', axis=1, inplace=True)
            linekeytabler_pk = linekeytable_pk.copy(deep=True)
            linekeytable_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] = linekeytable_pk
            return linekeytable_pk

        elif tablename.find('SpecRich')!=-1:
            fulldf = sperich_pk(dimapath)
            arc.isolateFields(fulldf, 'LineKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'LineKey':'LineKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['LineKey2'])
            linekeytable = arc.MakeTableView(f'{tablename}',dimapath)
            linekeytable_pk = lin.merge(linekeytable, left_on=lin.LineKey2, right_on=linekeytable.LineKey)
            linekeytable_pk.drop('LineKey2', axis=1, inplace=True)
            linekeytabler_pk = linekeytable_pk.copy(deep=True)
            linekeytable_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] = linekeytable_pk
            return linekeytable_pk

        elif tablename.find('PlantDen')!=-1:
            fulldf = plantden_pk(dimapath)
            arc.isolateFields(fulldf, 'LineKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'LineKey':'LineKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['LineKey2'])
            linekeytable = arc.MakeTableView(f'{tablename}',dimapath)
            linekeytable_pk = lin.merge(linekeytable, left_on=lin.LineKey2, right_on=linekeytable.LineKey)
            linekeytable_pk.drop('LineKey2', axis=1, inplace=True)
            linekeytabler_pk = linekeytable_pk.copy(deep=True)
            linekeytable_pk.drop('key_0', axis=1, inplace=True)
            return linekeytable_pk

    elif tablename in reckeylist:
        if tablename.find('Gap')!=-1:
            fulldf = gap_pk(dimapath)
            arc.isolateFields(fulldf, 'RecKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'RecKey':'RecKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['RecKey2'])
            reckeytable = arc.MakeTableView(f'{tablename}',dimapath)
            reckeytable_pk = lin.merge(reckeytable, left_on=lin.RecKey2, right_on=reckeytable.RecKey)
            reckeytable_pk.drop('RecKey2', axis=1, inplace=True)
            reckeytable_pk = reckeytable_pk.copy(deep=True)
            reckeytable_pk.drop('key_0', axis=1, inplace=True)
            return reckeytable_pk

        elif tablename.find('LPI')!=-1:
            fulldf = lpi_pk(dimapath)
            arc.isolateFields(fulldf, 'RecKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'RecKey':'RecKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['RecKey2'])
            reckeytable = arc.MakeTableView(f'{tablename}',dimapath)
            reckeytable_pk = lin.merge(reckeytable, left_on=lin.RecKey2, right_on=reckeytable.RecKey)
            reckeytable_pk.drop('RecKey2', axis=1, inplace=True)
            reckeytable_pk = reckeytable_pk.copy(deep=True)
            reckeytable_pk.drop('key_0', axis=1, inplace=True)
            return reckeytable_pk

        elif tablename.find('SpecRich')!=-1:
            fulldf = sperich_pk(dimapath)
            arc.isolateFields(fulldf, 'RecKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'RecKey':'RecKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['RecKey2'])
            reckeytable = arc.MakeTableView(f'{tablename}',dimapath)
            reckeytable_pk = lin.merge(reckeytable, left_on=lin.RecKey2, right_on=reckeytable.RecKey)
            reckeytable_pk.drop('RecKey2', axis=1, inplace=True)
            reckeytable_pk = reckeytable_pk.copy(deep=True)
            reckeytable_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] = reckeytable_pk
            return reckeytable_pk

        elif tablename.find('PlantDen')!=-1:
            fulldf = plantden_pk(dimapath)
            arc.isolateFields(fulldf, 'RecKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'RecKey':'RecKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['RecKey2'])
            reckeytable = arc.MakeTableView(f'{tablename}',dimapath)
            reckeytable_pk = lin.merge(reckeytable, left_on=lin.RecKey2, right_on=reckeytable.RecKey)
            reckeytable_pk.drop('RecKey2', axis=1, inplace=True)
            reckeytable_pk = reckeytable_pk.copy(deep=True)
            reckeytable_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] = reckeytable_pk
            return reckeytable_pk

        else:
            tempdf = arc.MakeTableView(nonline[f'{tablename}'], dimapath)
            fulldf = arc.CalculateField(tempdf, "PrimaryKey", "PlotKey", "FormDate")
            arc.isolateFields(fulldf, 'RecKey','PrimaryKey')
            line_tmp = arc.isolates
            lin = line_tmp.rename(columns={'RecKey':'RecKey2'}).copy(deep=True)
            lin = lin.drop_duplicates(['RecKey2'])
            reckeytable = arc.MakeTableView(f'{tablename}',dimapath)
            reckeytable_pk = lin.merge(reckeytable, left_on=lin.RecKey2, right_on=reckeytable.RecKey)
            reckeytable_pk.drop('RecKey2', axis=1, inplace=True)
            reckeytable_pk = reckeytable_pk.copy(deep=True)
            reckeytable_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] = reckeytable_pk
            return reckeytable_pk

    elif tablename.find("BSNE")!=-1:
        if tablename.find("Stack")!=-1:
            tempdf = arc.MakeTableView(f'{tablename}', dimapath)
            fulldf = bsne_pk(dimapath)
            arc.isolateFields(fulldf, 'PlotKey','PrimaryKey')
            plot_tmp = arc.isolates
            plt = plot_tmp.rename(columns={'PlotKey':'PlotKey2'}).copy(deep=True)
            plt = plt.drop_duplicates(['PlotKey2'])
            plottable = arc.MakeTableView(f'{tablename}',dimapath)
            plot_pk = plt.merge(plottable, left_on=plt.PlotKey2, right_on=plottable.PlotKey)
            plot_pk.drop('PlotKey2', axis=1, inplace=True)
            plot_pk = plot_pk.copy(deep=True)
            plot_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] =plot_pk
            return plot_pk

        if tablename.find("BoxCollection")!=-1:
            tempdf = arc.MakeTableView(f'{tablename}', dimapath)
            fulldf = bsne_pk(dimapath)
            arc.isolateFields(fulldf, 'BoxID','PrimaryKey')
            plot_tmp = arc.isolates
            plt = plot_tmp.rename(columns={'BoxID':'BoxID2'}).copy(deep=True)
            plt = plt.drop_duplicates(['BoxID2'])
            plottable = arc.MakeTableView(f'{tablename}',dimapath)
            plot_pk = plt.merge(plottable, left_on=plt.BoxID2, right_on=plottable.BoxID)
            plot_pk.drop('BoxID2', axis=1, inplace=True)
            plot_pk = plot_pk.copy(deep=True)
            plot_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] =plot_pk
            return plot_pk

        elif tablename.find("Trap")!=-1: # added
            tempdf = arc.MakeTableView(f'{tablename}', dimapath)
            fulldf = bsne_pk(dimapath)
            arc.isolateFields(fulldf, 'StackID','PrimaryKey')
            stack_tmp = arc.isolates
            stk = stack_tmp.rename(columns={'StackID':'StackID2'}).copy(deep=True)
            stk = stk.drop_duplicates(['StackID2'])
            stacktable = arc.MakeTableView(f'{tablename}',dimapath)
            stack_pk = stk.merge(stacktable, left_on=stk.StackID2, right_on=stacktable.StackID)
            stack_pk.drop('StackID2', axis=1, inplace=True)
            stack_pk = stack_pk.copy(deep=True)
            stack_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] =plot_pk
            return stack_pk

        else:
            tempdf = arc.MakeTableView(f'{tablename}', dimapath)
            fulldf = bsne_pk(dimapath)
            arc.isolateFields(fulldf, 'BoxID','PrimaryKey')
            plot_tmp = arc.isolates
            plt = plot_tmp.rename(columns={'BoxID':'BoxID2'}).copy(deep=True)
            plt = plt.drop_duplicates(['BoxID2'])
            plottable = arc.MakeTableView(f'{tablename}',dimapath)
            plot_pk = plt.merge(plottable, left_on=plt.BoxID2, right_on=plottable.BoxID)
            plot_pk.drop('BoxID2', axis=1, inplace=True)
            plot_pk = plot_pk.copy(deep=True)
            plot_pk.drop('key_0', axis=1, inplace=True)
            # mdb[f'{tablename}'] =plot_pk
            return plot_pk
    elif (tablename.find('tblSpecie')!=-1) or (tablename.find('tblSpeciesGeneric')!=-1) or (tablename.find('tblSites')!=-1):
        tempdf = arc.MakeTableView(f'{tablename}', dimapath)
        return tempdf

    else:
        # print('Supplied tablename does not exist in dima or a path to it has not been implemented.')

        tempdf = arc.MakeTableView(f'{tablename}', dimapath) # added
        return tempdf

def newcols(fdf,rdf):
    for item in fdf.columns.tolist():
        if item not in rdf.columns.tolist():
            df = rdf.copy(deep=True)
            df[f'{item}'] = fdf[f'{item}']
            return df


def pg_send(tablename, dimapath):
    mwacksig = 0
    ddtsig = 0
    cursor = db.str.cursor()
    try:
        # adds primarykey to access table and returns dataframe with it
        # if its a box, box collection or ddt table, bring full df
        if (tablename.find('BSNE_Box')!=-1) or (tablename.find('BSNE_BoxCollection')!=-1) or (tablename.find('BSNE_TrapCollection')!=-1):
            df = bsne_pk(dimapath)
        else:
            df = pk_add(tablename,dimapath)


        # adds dateloaded and db key to dataframe
        df['DateLoadedInDB']= datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if dimapath.find('calibration')!=-1:

            df['DBKey']=join('calibration_',split(splitext(dimapath.replace('Calibration','').replace('calibration',''))[0])[1].replace(" ",""))
            df['DBKey']=split(splitext(dimapath)[0])[1].replace(" ","")
        else:
            df['DBKey']=split(splitext(dimapath)[0])[1].replace(" ","")

        if 'ItemType' in df.columns:
            #handles mwack or ddt names, turns on signals for further processing
            if (df.ItemType[0]=='M') or (df.ItemType[0]=='m'):
                mwacksig = 1
                # if tablename.find('Stack')!=-1:
                #     # newtablename = 'tblHorizontalFlux_Locations'
                # else:
                newtablename = 'tblHorizontalFlux'

            elif (df.ItemType[0]=='T') or (df.ItemType[0]=='t'):
                ddtsig = 1
                # if tablename.find('Stack')!=-1:
                #     # newtablename = 'tblDustDeposition_Locations'
                # else:
                newtablename = 'tblDustDeposition'
        else:
            pass

        # use pandas 'to_sql' to send altered dataframe to postgres db
        engine = create_engine(sql_str(config()))
        if df.shape[0]>0:
            # need to pull col list from db
            try:
            #if theres no difference, ingest and append, else do the magic
                while (mwacksig == 0) and (ddtsig == 0):
                    # if mwack or ddt signals off, ingest normally
                    df.to_sql(name=f'{tablename}',con=engine, index=False, if_exists='append')
                    break
                else:
                    if tablename.find('Stack')!=-1:
                        pass
                    else:
                        tablename = newtablename
                        df.to_sql(name=f'{tablename}',con=engine, index=False, if_exists='append')
                        mwacksig = 0
                        ddtsig = 0


            except Exception as e:
                # handling out of norm table schemas..
                print("mismatch between the columns in database table and supplied table..")

                dbcols = pd.read_sql(f'SELECT * FROM "{tablename}" LIMIT 1', db.str)


                if len(df.columns.tolist())>1:
                    # if df has anything in it...
                    for item in df.columns.tolist():
                        if item not in dbcols.columns.tolist():
                            # any column not in the database has to be
                            # created: colname + postgres-compatible datatype
                            print(f'{item} is not in db')
                            vartype = {
                            'int64':'int',
                            "object":'text',
                            'datetime64[ns]':'timestamp',
                            'bool':'boolean',
                            'float64':'float'
                            }

                            cursor.execute("""
                            ALTER TABLE "%s" ADD COLUMN "%s" %s
                            """ % (f'{tablename}',f'{item}',vartype[f'{df[f"{item}"].dtype}'].upper()))
                            db.str.commit()

                df.to_sql(name=f'{tablename}',con=engine, index=False, if_exists='append')

        else:
            print(f'Ingestion to postgresql DB aborted: {tablename} is empty')

    except Exception as e:
        print(e)

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
