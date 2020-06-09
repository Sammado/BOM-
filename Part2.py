#Import necessary libraries
import pandas as pd
import numpy as np
from pathlib import Path


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
path0=r'C:\Users\user\Desktop\BOM_Project\ICIM-E10P bom for PX1-I440-ADC-4201 (3).xlsx'
path=r'C:\Users\user\Desktop\BOM_Project\ICIM-E10P bom for PX1-I440-ADC-420 (3).xlsx'
path2=r'C:\Users\user\Desktop\BOM_Project\ICM-E10L Load of ITX-P-C444-PP1 (3).csv'
path3=r'C:\Users\user\Desktop\BOM_Project\PNP Data format BOM for PX1-I440 (1).csv'
#A function that detect the type of the file
def type_file(path):
    if Path(path).suffix=='.csv':
        dataframe=pd.read_csv(path)
        if dataframe.shape[1]==6:
            return('type 3')
        else:
            return('type 2')
    else:
        return('type 1')

#Conversion of all files
def conv(path):
    if type_file(path)=='type 1':
        return(pd.read_excel(path,sheetname=0,header=1))
    elif type_file(path)=='type 2':
        return(pd.read_csv(path))
    else:
        dataframe=pd.read_csv(path,names=['Center-X(Mil)','Center-Y(Mil)','Rotation','Designator','ICIM_PART_NUM','Layer'],comment='!')
        isnotnan=lambda x: not(np.isnan(x))
        return(dataframe[dataframe['Center-X(Mil)'].apply(isnotnan)])

#a function  to combine two boms
def combine1(path_E10P,path_PNP):
    bom1=conv(path_E10P)
    bom2=conv(path_PNP)
    bom2.rename(columns={'ICIM_PART_NUM':'Component Part'},inplace=True)
    result=pd.merge(bom1,bom2,on='Component Part')
    result=result.drop_duplicates(keep=False)
    print(result)

#A function to substract two BOMs
def sub_BOM(path_Bom1,path_Bom2):
    typef=type_file(path_Bom1)
    bom1=conv(path_Bom1)
    bom2=conv(path_Bom2)
    col=bom1.columns
    col=col.tolist()
    print(col)
    bom1=bom1.values.tolist()
    bom2=bom2.values.tolist()
    L=[]
    if typef=='type 1':
        for i in bom1:
            add=1
            for j in bom2:
                if i[1]==j[1]:
                    add=0
            if add==1 and i not in L:
                L.append(i)
        for i in bom2:
            add=1
            for j in bom1:
                if i[1]==j[1]:
                    add=0
            if add==1 and i not in L:
                L.append(i)
    if typef=='type 3':
        for i in bom1:
            add=1
            for j in bom2:
                if i[4]==j[4]:
                    add=0
            if add==1 and i not in L:
                L.append(i)
        for i in bom2:
            add=1
            for j in bom1:
                if i[4]==j[4]:
                    add=0
            if add==1 and i not in L:
                L.append(i)
    return(pd.DataFrame(L,columns=col))

