import pandas as pd

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

def process_vitals(vitals_df):
   # Remove values before admit to hospital
   new_vitals_df = vitals_df[vitals_df['admit_time_day'] >= 0]
   # Get Min and Max and rename what will be new columns
   min_vitals_df = new_vitals_df.loc[new_vitals_df.groupby(['deid','risk_factor'])['admit_time_day'].idxmin()]   
   min_vitals_df['risk_factor'] = 'V ' + min_vitals_df['risk_factor'] + ' 1' 
   max_vitals_df = new_vitals_df.loc[new_vitals_df.groupby(['deid','risk_factor'])['admit_time_day'].idxmax()]
   max_vitals_df['risk_factor'] = 'V ' + max_vitals_df['risk_factor'] + ' 2'
   new_vitals_df = min_vitals_df.append(max_vitals_df)
   # Remove columns not needed
   new_vitals_df = new_vitals_df.drop(['admit_day','admit_time_day'], 1)
   # Pivot
   new_vitals_df = new_vitals_df.pivot_table(index='deid', columns='risk_factor', aggfunc='first')
   # Sort columns to get 1st and last day together
   new_vitals_df = new_vitals_df.reindex(sorted(new_vitals_df.columns), axis=1)
   new_vitals_df = new_vitals_df.xs('result', axis=1, drop_level=True)
   
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
   #right_df = right_df.drop(['index'], 1)
   left_df.reset_index(inplace=True)
   left_df.set_index(join_index, inplace=True)  
   #left_df = left_df.drop(['index'], 1)   
   joined_df = left_df.join(right_df, how='left')
   return joined_df
   
if __name__== "__main__":
   vitals_df = read_to_df('../data_in/vitals_extract_GT.csv')

   
   #ranges_df = read_to_df('../data_in/normal_ranges.csv')
   #lab_ranges_df = ranges_df[ranges_df['dataset'] == 'lab']
   #vitals_ranges_df = ranges_df[ranges_df['dataset'] == 'vitals']
   #test_df = join_dataframes(vitals_df,vitals_ranges_df,['risk_factor'])
   #test_df.loc[test_df['result'] < test_df['low'], 'range'] == -1
   #test_df.loc[test_df['result'] > test_df['high'], 'range'] == 1
   #print (vitals_ranges_df)
   #print (vitals_df)
   #print (test_df)
   
   vitals_df = process_vitals(vitals_df)
   write_df('../data_out/vitals_extract_GT_pivot.csv',vitals_df)
   main_df = read_to_df('../data_in/main_extract_GT.csv')
   main_by_day_df = main_by_day(main_df)
   write_df('../data_out/main_by_day.csv',main_by_day_df)
   # Join to make it deid, admit_day
   main_joined_df = join_dataframes(main_df,main_by_day_df,'deid')
   # Join main to vitals deid, admit_day
   main_joined_df = join_dataframes(main_joined_df,vitals_df,['deid','admit_day'])
   #write_df('../data_out/join_vitals.csv',main_joined_df)
   #
   labs_df = read_to_df('../data_in/Lab_extract_GT.csv')
   labs_df = process_labs(labs_df)
   write_df('../data_out/Lab_extract_GT_pivot.csv',labs_df)
   main_joined_df = join_dataframes(main_joined_df,labs_df,['deid','admit_day'])
   #write_df('../data_out/join4.csv',main_joined_df)   
   #
   images_df = read_to_df('../data_in/images_extract_GT.csv')
   images_df = process_images(images_df)
   write_df('../data_out/images_extract_GT_pivot.csv',images_df)
   main_joined_df = join_dataframes(main_joined_df,images_df,['deid','admit_day'])
   #write_df('../data_out/join5.csv',main_joined_df)      
   #
   medications_df = read_to_df('../data_in/Mar_GT.csv')
   medications_df = process_medications(medications_df)
   write_df('../data_out/medications_extract_GT_pivot.csv',images_df)
   main_joined_df = join_dataframes(main_joined_df,medications_df,['deid','admit_day'])
   #write_df('../data_out/join6.csv',main_joined_df)  
   #
   transfuse_df = read_to_df('../data_in/transfuse_extract_GT.csv')
   transfuse_df = process_transfuse(transfuse_df)
   write_df('../data_out/transfuse_extract_GT_pivot.csv',transfuse_df)
   main_joined_df = join_dataframes(main_joined_df,transfuse_df,['deid','admit_day'])
   write_df('../data_out/joined.csv',main_joined_df)    