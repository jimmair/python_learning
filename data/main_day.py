import pandas as pd

main_df = pd.read_csv('./csv_data/main_extract_GT_small.csv')
#deid_day_df = pd.DataFrame(['deid','admit_day'])
deid_day_df = pd.DataFrame()
#deid_day_df.set_index('deid', inplace=True)
for index, row in main_df.iterrows():
   for x in range(0, row['los']+1):
      deid_day_df = deid_day_df.append([{'deid': row['deid'],'admit_day': x}],ignore_index=True)

deid_day_df.set_index('deid', inplace=True)
deid_day_df.to_csv('./csv_data/main_by_day.csv')