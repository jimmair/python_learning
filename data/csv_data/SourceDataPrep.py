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
   
def process_images(images_df):
   # Remove columns not needed
   new_images_df = images_df.drop(['procedure_clinic_desc'], 1)
   new_images_df['Indicator'] = 1
   # Aggregate only keeping the 1st value
   new_images_df = new_images_df.pivot_table(index=['deid','admit_day'], columns='cpt', aggfunc='first')
   # Rename the risk_factor column headers to be "lab [l_value]"
   new_images_df.columns = [" ".join(('image cpt',str(j))) for i,j in new_images_df.columns]
   # Remove the hierarchy of indexes to be no index
   new_images_df.reset_index()
   return new_images_df   
   
def process_medications(medications_df):
   # Remove columns not needed
   new_medications_df = medications_df.drop(['admit_to_mar_ts','op_to_order','op_to_mar','route_medication_desc','prn_ind','prn_ind_desc','order_catalog_desc'], 1)
   new_medications_df['Indicator'] = 1
   # Rename to match join column
   new_medications_df.rename(columns={'admit_to_mar_dt':'admit_day'}, inplace=True)
   # Aggregate only keeping the 1st value
   new_medications_df = new_medications_df.pivot_table(index=['deid','admit_day'], columns='order_catalog_id', aggfunc='sum')
   # Rename the risk_factor column headers to be "Medication [order_catalog_id]"
   new_medications_df.columns = [" ".join(('medication id',str(j))) for i,j in new_medications_df.columns]
   # Remove the hierarchy of indexes to be no index
   new_medications_df.reset_index()
   return new_medications_df      
   
def process_transfuse(transfuse_df):
   # Remove columns not needed
   new_transfuse_df = transfuse_df.drop(['admit_to_order_ts'], 1)
   new_transfuse_df['Indicator'] = 1
   # Rename to match join column
   new_transfuse_df.rename(columns={'admit_to_order_dt':'admit_day'}, inplace=True)
   # Aggregate only keeping the 1st value
   new_transfuse_df = new_transfuse_df.pivot_table(index=['deid','admit_day'], columns='order_catalog_desc', aggfunc='sum')
   # Rename the risk_factor column headers to be "Transfuse name"
   new_transfuse_df.columns = [" ".join(('',str(j))) for i,j in new_transfuse_df.columns]   
   # Remove the hierarchy of indexes to be no index
   new_transfuse_df.reset_index()
   return new_transfuse_df       
   
def join_dataframes(left_df,right_df,join_index):
   # set the join_index on both dataframes
   right_df.reset_index(inplace=True)
   right_df.set_index(join_index, inplace=True) 
   right_df = right_df.drop(['index'], 1)
   left_df.reset_index(inplace=True)
   left_df.set_index(join_index, inplace=True)  
   left_df = left_df.drop(['index'], 1)   
   joined_df = left_df.join(right_df, how='left')
   return joined_df
   
if __name__== "__main__":
   vitals_df = read_to_df('../csv_data/vitals_extract_GT.csv')

   
   #ranges_df = read_to_df('../csv_data/normal_ranges.csv')
   #lab_ranges_df = ranges_df[ranges_df['dataset'] == 'lab']
   #vitals_ranges_df = ranges_df[ranges_df['dataset'] == 'vitals']
   #test_df = join_dataframes(vitals_df,vitals_ranges_df,['risk_factor'])
   #test_df.loc[test_df['result'] < test_df['low'], 'range'] == -1
   #test_df.loc[test_df['result'] > test_df['high'], 'range'] == 1
   #print (vitals_ranges_df)
   #print (vitals_df)
   #print (test_df)
   
   vitals_df = process_vitals(vitals_df)
   write_df('../csv_data/vitals_extract_GT_new.csv',vitals_df)
   #main_df = read_to_df('../csv_data/main_extract_GT_small.csv')
   #main_by_day_df = main_by_day(main_df)
   #write_df('../csv_data/main_by_day.csv',main_by_day_df)
   ## Join to make it deid, admit_day
   #main_joined_df = join_dataframes(main_df,main_by_day_df,'deid')
   #write_df('../csv_data/join2.csv',main_joined_df)
   ## Join main to vitals deid, admit_day
   #main_joined_df = join_dataframes(main_joined_df,vitals_df,['deid','admit_day'])
   #write_df('../csv_data/join3.csv',main_joined_df)
   #
   #labs_df = read_to_df('../csv_data/Lab_extract_GT_small.csv')
   #labs_df = process_labs(labs_df)
   #write_df('../csv_data/Lab_extract_GT_new.csv',labs_df)
   #main_joined_df = join_dataframes(main_joined_df,labs_df,['deid','admit_day'])
   #write_df('../csv_data/join4.csv',main_joined_df)   
   #
   #images_df = read_to_df('../csv_data/images_extract_GT_small.csv')
   #images_df = process_images(images_df)
   #write_df('../csv_data/images_extract_GT_new.csv',images_df)
   #main_joined_df = join_dataframes(main_joined_df,images_df,['deid','admit_day'])
   #write_df('../csv_data/join5.csv',main_joined_df)      
   #
   #medications_df = read_to_df('../csv_data/Mar_GT_small.csv')
   #medications_df = process_medications(medications_df)
   #write_df('../csv_data/medications_extract_GT_new.csv',images_df)
   #main_joined_df = join_dataframes(main_joined_df,medications_df,['deid','admit_day'])
   #write_df('../csv_data/join6.csv',main_joined_df)  
   #
   #transfuse_df = read_to_df('../csv_data/transfuse_extract_GT_small.csv')
   #transfuse_df = process_transfuse(transfuse_df)
   #write_df('../csv_data/transfuse_extract_GT_new.csv',transfuse_df)
   #main_joined_df = join_dataframes(main_joined_df,transfuse_df,['deid','admit_day'])
   #write_df('../csv_data/join7.csv',main_joined_df)    