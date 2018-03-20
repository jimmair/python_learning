import pandas as pd

def read_to_df(read_filename):
   read_df = pd.read_csv(read_filename)
   return read_df
   
def write_df(write_filename, write_df):
   write_df.to_csv(write_filename)   

def main_by_day(main_df):
   new_main_df = pd.DataFrame()
   for index, row in main_df.iterrows():
      for x in range(0, row['los']+1):
         new_main_df = new_main_df.append([{'deid': row['deid'],'admit_day': x}],ignore_index=True)
   new_main_df.set_index('deid', inplace=True)
   return new_main_df

def process_vitals(vitals_df):
   # Remove columns not needed
   new_vitals_df = vitals_df.drop('admit_time_day', 1)
   # Aggregate only keeping the 1st value
   new_vitals_df = new_vitals_df.pivot_table(index=['deid','admit_day'], columns='risk_factor', aggfunc='first')
   # Rename the risk_factor column headers to be "vital [risk_factor]"
   new_vitals_df.columns = [" ".join(('vital',j)) for i,j in new_vitals_df.columns]
   # Remove the hierarchy of indexes to be no index
   new_vitals_df.reset_index()
   return new_vitals_df
   
def process_labs(labs_df):
   # Remove columns not needed
   new_labs_df = labs_df.drop(['structured_result_type_id','structured_result_type_cd','structured_result_type_desc',
'admit_time_day'], 1)
   # Aggregate only keeping the 1st value
   new_labs_df = new_labs_df.pivot_table(index=['deid','admit_day'], columns='risk_factor', aggfunc='first')
   # Rename the risk_factor column headers to be "lab [l_value]"
   new_labs_df.columns = [" ".join(('lab',j)) for i,j in new_labs_df.columns]
   # Remove the hierarchy of indexes to be no index
   new_labs_df.reset_index()
   return new_labs_df
   
def join_dataframes(left_df,right_df,join_index):
   # set the join_index on both dataframes
   right_df.reset_index(inplace=True)
   right_df.set_index(join_index, inplace=True)   
   left_df.reset_index(inplace=True)
   left_df.set_index(join_index, inplace=True)   
   joined_df = left_df.join(right_df, how='left')
   return joined_df
   
if __name__== "__main__":
   vitals_df = read_to_df('../csv_data/vitals_extract_GT_small.csv')
   vitals_df = process_vitals(vitals_df)
   write_df('../csv_data/vitals_extract_GT_new.csv',vitals_df)
   main_df = read_to_df('../csv_data/main_extract_GT_small.csv')
   main_by_day_df = main_by_day(main_df)
   write_df('../csv_data/main_by_day.csv',main_by_day_df)
   # Join to make it deid, admit_day
   main_joined_df = join_dataframes(main_df,main_by_day_df,'deid')
   write_df('../csv_data/join2.csv',main_joined_df)
   # Join main to vitals deid, admit_day
   main_joined_df = join_dataframes(main_joined_df,vitals_df,['deid','admit_day'])
   write_df('../csv_data/join3.csv',main_joined_df)
   
   labs_df = read_to_df('../csv_data/Lab_extract_GT_small.csv')
   labs_df = process_labs(labs_df)
   write_df('../csv_data/Lab_extract_GT_new.csv',labs_df)
   main_joined_df = join_dataframes(main_joined_df,labs_df,['deid','admit_day'])
   write_df('../csv_data/join4.csv',main_joined_df)   