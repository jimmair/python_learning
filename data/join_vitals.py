import pandas as pd

main_df = pd.read_csv('./csv_data/join.csv')
main_df.set_index(['deid','admit_day'], inplace=True)

vital_df = pd.read_csv('./csv_data/vitals_extract_GT_new.csv')
vital_df.set_index(['deid','admit_day'], inplace=True)
#vital_df = vital_df.unstack(level=-1)

#print (main_df.index.tolist())
#print (vital_df.index.tolist())
#print (vital_df[:5])
#print (main_by_day_df)

result = main_df.join(vital_df, how='left')


#print (list(result.index.values))
#result.reset_index()
#result.set_index(['deid'], inplace=True)
#result2 = result.join(vital_df, how='left')
#result = pd.merge(main_df, vital_df, left_index=True, right_index=True, how='outer')
result.to_csv('./csv_data/join_vitals.csv')