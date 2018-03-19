import pandas as pd
import os
import glob


def read_data():
    base_dir = './csv_data'
    allFiles = glob.glob(base_dir+"/*.csv")
    fileNames = []
    dict_dataframe = {}
    for file in allFiles:
        base = os.path.basename(file)
        fileName = os.path.splitext(base)[0]
        fileNames.append(fileName)
        df_temp = pd.read_csv(file, index_col='deid')
        df =df_temp.sort_index(level='deid')
        dict_dataframe[fileName] = df
        print (fileNames)
    #print  "file name list: ", fileNames, "\ntotal file read: ", len(dict_dataframe), "\n", dict_dataframe
if __name__ == "__main__":
    read_data()