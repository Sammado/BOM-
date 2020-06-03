#Import necessary libraries
import pandas as pd
import numpy as np
from pathlib import Path


pd.set_option('display.max_columns', None)
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



print(conv(path))