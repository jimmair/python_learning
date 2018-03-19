import pandas as pd

main_df = pd.read_csv('./csv_data/main_extract_GT_small.csv')
main_df.set_index('deid', inplace=True)

main_by_day_df = pd.read_csv('./csv_data/main_by_day.csv')
main_by_day_df.set_index('deid', inplace=True)

#vital_df = pd.read_csv('./csv_data/vitals_extract_GT_new3.csv')
#vital_df.set_index(('deid','admit_day'), inplace=True)
#vital_df = vital_df.unstack(level=-1)
#print (main_df.index.tolist())
#rint (vital_df.index.tolist())
#print (vital_df[:5])
result = main_by_day_df.join(main_df, how='left')
print (list(result.columns.values))
result.reset_index()
result.set_index(['deid'], inplace=True)
#result2 = result.join(vital_df, how='left')
#result = pd.merge(main_df, vital_df, left_index=True, right_index=True, how='outer')
result.to_csv('./csv_data/join.csv')