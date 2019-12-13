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
"""

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

str = sys.argv[1]



class arcno():
    tablelist = []
    isolates = None

    def __init__(self, whichdima = None):
        """ Initializes a list of tables in dima accessible on tablelist.
        ex.
        arc = arcno(path_to_dima)
        arc.tablelist
        """
        self.whichdima = whichdima
        if self.whichdima is not None:
            cursor = Acc(self.whichdima).con.cursor()
            for t in cursor.tables():
                if t.table_name.startswith('tbl'):
                    self.tablelist.append(t.table_name)


    def MakeTableView(self,in_table,whichdima):
        """ connects to Microsoft Access .mdb file, selects a table
        and copies it to a dataframe.
        ex.
        arc = arcno()
        arc.MakeTableView('table_name', 'dima_path')
        """
        self.in_table = in_table
        self.whichdima = whichdima

        try:
            return Table(self.in_table, self.whichdima).temp
        except Exception as e:
            print(e)

    def SelectLayerByAttribute(self, in_df,*vals, field = None):

        import pandas as pd
        self.in_df = in_df
        self.field = field
        self.vals = vals

        dfset = []
        def name(arg1,arg2):
            self.arg1 = arg1
            self.arg2 = arg2
            import os
            joined= os.path.join(self.arg1+self.arg2)
            return joined

        if all(self.in_df):
            print("dataframe exists")
            try:
                for val in self.vals:
                    index = self.in_df[f'{self.field}']==f'{val}'
                    exec("%s = self.in_df[index]" % name(f'{self.field}',f'{val}'))
                    dfset.append(eval(name(f'{self.field}',f'{val}')))

                return pd.concat(dfset)
            except Exception as e:
                print(e)
        else:
            print("error")
    def GetCount(self,in_df):
        """ Returns number of rows in dataframe
        """
        self.in_df = in_df
        return self.in_df.shape[0]

    def AddJoin(self,
    in_df,df2,right_on=None,left_on=None):
        """ inner join on two dataframes on 1 or 2 fields
        ex.
        arc = arcno()
        arc.AddJoin('dataframe_x', 'dataframe_y', 'field_a')
        """
        # self.temp_table = None
        d={}
        self.right_on = None
        self.left_on = None

        d[self.right_on] = right_on
        d[self.left_on] = left_on

        self.in_df = in_df
        self.df2 = df2

        if self.right_on==self.left_on and len(self.in_df.columns)==len(self.df2.columns):
            try:
                frames = [self.in_df, self.df2]
                return pd.concat(frames)
            except Exception as e:
                print(e)
                print('1. field or fields invalid' )
        elif self.right_on==self.left_on and len(self.in_df.columns)!=len(self.df2.columns):
            try:
                # frames = [self.in_df, self.df2]
                return self.in_df.merge(self.df2, on = d[self.right_on], how='inner')
            except Exception as e:
                print(e)
                print('2. field or fields invalid')
        else:
            try:
                return self.in_df.merge(self.df2,right_on=d[self.right_on], left_on=d[self.left_on])
            except Exception as e:
                print(e)
                print('3. field or fields invalid')

    def CalculateField(self,in_df,newfield,*fields):
        """ Creates a newfield by concatenating any number of existing fields
        ex.
        arc = arcno()
        arc.CalculateField('dataframe_x', 'name_of_new_field', 'field_x', 'field_y','field_z')
        field_x = 'red'
        field_y = 'blue'
        field_z = 'green'
        name_of_new_field = 'redbluegreen'
        """
        self.in_df = in_df
        self.newfield = newfield
        self.fields = fields

        self.in_df[f'{self.newfield}'] = (self.in_df[[f'{field}' for field in self.fields]].astype('object')).sum(axis=1)
        return self.in_df



    def AddField(self, in_df, newfield):
        """ adds empty field within 'in_df' with fieldname
        supplied in the argument
        """
        self.in_df = in_df
        self.newfield = newfield

        self.in_df[f'{self.newfield}'] = pd.Series()
        return self.in_df

    def RemoveJoin(self):
        """ creates deep copy of original dataset
        and joins any new fields product of previous
        right hand join
        """
        pass

    def isolateFields(self,in_df,*fields):
        """ creates a new dataframe with submitted
        fields.
        """
        self.in_df = in_df
        self.fields = fields
        self.isolates =self.in_df[[f'{field}' for field in self.fields]]
        return self.isolates


    def GetParameterAsText(self,string):
        """ return stringified element
        """
        self.string = f'{string}'
        return self.string

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




# a=arc.MakeTableView('tblGapDetail', path)
# b=arc.MakeTableView('tblGapHeader', path)
#
# c=arc.MakeTableView('tblLines',path)
# d=arc.MakeTableView('tblPlots',path)
#
# e=arc.AddJoin(c,d, 'PlotKey', 'PlotKey')
# f = arc.AddJoin(a,b, 'RecKey')
# g.
# g = arc.AddJoin(e,f, 'LineKey', 'LineKey')


# self.in_df = in_df
# self.newfield = newfield
# self.fields = fields
#
# self.in_df[f'{self.newfield}'] = (self.in_df[[f'{field}' for field in self.fields]].astype(str)).sum(axis=1)
#
# def fun1(dataframe, name, fields*):
#     pass
#
# g2 = arc.CalculateField(g,"PrimaryKey","PlotKey","FormDate")
#
#
# listd = ['a','b']
# df = pd.DataFrame(
# {'a':['one','two'],
# 'b':['three','four']
# })
#
# df[['a']]
# df['newfield']=df[[f'{i}'for i in listd]].sum(axis=1)
#
#



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
    arc = arcno()
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

def pk_add(tablename,dimapath):
    """
    adds primary key to the chosen table
    1. PlotKey pipe
    2. LineKey pipe
    3. reckey pipe
    4. pipe if its none of the above: only BSNE implemented
    """
    # plot = None


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
            linekeytable_pk = linekeytable_pk.copy(deep=True)
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
        if (dimapath.find('calibration')!=-1) or (dimapath.find('Calibration')!=-1):

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

def sql_str(args):
    strg = join('postgresql://'+args['user']+':'+args['password']+'@'+args['host']+'/'+args['dbname'])
    return strg

class Acc:
    con=None
    def __init__(self, whichdima):
        self.whichdima=whichdima
        MDB = self.whichdima
        DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        mdb_string = r"DRIVER={};DBQ={};".format(DRV,MDB)
        self.con = pyodbc.connect(mdb_string)

    def db(self):
        try:
            return self.con
        except Exception as e:
            print(e)

class Table:
    temp=None
    def __init__(self,in_table=None, path=None):
        self.path = path
        self.in_table = in_table
        con = Acc(self.path).con
        query = f'SELECT * FROM "{self.in_table}"'
        self.temp = pd.read_sql(query,con)

    def temp(self):
        return self.temp

try:
    for table in maintablelist:
        pg_send(f'{table}',str)
    print(f'dima "{splitext(basename(str))[0]}" was uploaded!')
    # print(config())
except Exception as e:
    print(e)

sys.stdout.flush()
