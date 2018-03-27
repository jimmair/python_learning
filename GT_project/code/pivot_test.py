import pandas as pd
import numpy as np

def read_to_df(read_filename):
   read_df = pd.read_csv(read_filename)
   return read_df
   
def write_df(write_filename, write_df):
   write_df.to_csv(write_filename)   

def main_by_day(main_df):
   # Fill empty los (length of stay) with zero
   main_df['los'].fillna(0, inplace=True)
   # LOS needs to be an integer
   main_df['los'] = main_df.los.astype(int)
   new_main_df = pd.DataFrame()
   for index, row in main_df.iterrows():
      for x in range(0, (row['los']+1)):
         new_main_df = new_main_df.append([{'deid': row['deid'],'admit_day': x}],ignore_index=True)
   new_main_df.set_index('deid', inplace=True)
   return new_main_df

   
if __name__== "__main__":
   vitals_df = read_to_df('../data_in/vitals_extract_GT_small.csv')
   print (vitals_df)

   #new_vitals_df = vitals_df.drop('admit_day', 1)
   new_vitals_df = vitals_df
   
   new_vitals_df = new_vitals_df[new_vitals_df['admit_time_day'] >= 0]
   #new_vitals_df = new_vitals_df .groupby(['deid','risk_factor'], sort=False)['admit_day'].max()
   print (new_vitals_df[:5])
   min_vitals_df = new_vitals_df.loc[new_vitals_df.groupby(['deid','risk_factor'])['admit_time_day'].idxmin()]   
   min_vitals_df['risk_factor'] = 'V ' + min_vitals_df['risk_factor'] + ' 1' 
   max_vitals_df = new_vitals_df.loc[new_vitals_df.groupby(['deid','risk_factor'])['admit_time_day'].idxmax()]
   max_vitals_df['risk_factor'] = 'V ' + max_vitals_df['risk_factor'] + ' 2'
   print (max_vitals_df[:5])
   newer_vitals_df = min_vitals_df.append(max_vitals_df)

   #vitals_df[vitals_df['vital hr'].astype(str).str.isdigit()]
   newer_vitals_df = newer_vitals_df.drop(['admit_day','admit_time_day'], 1)
   print (newer_vitals_df[:5])
   newer_vitals_df = newer_vitals_df.pivot_table(index='deid', columns='risk_factor', aggfunc='first')
   print (newer_vitals_df[:5])
   newer_vitals_df = newer_vitals_df.reindex(sorted(newer_vitals_df.columns), axis=1)
   newer_vitals_df = newer_vitals_df.xs('result', axis=1, drop_level=True)
   #newer_vitals_df.set_index('deid', inplace=True)
   print (newer_vitals_df[:5])

   
   write_df('../data_out/vitals_extract_GT_pivot2.csv',newer_vitals_df)
  