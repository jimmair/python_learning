import pandas as pd
import numpy as np
#read_csv
df = pd.read_csv('./csv_data/vitals_extract_GT_small.csv')
print (df)
df = df.drop('admit_time_day', 1)
print (df)
#df.set_index(['deid','admit_day'], inplace=True)
#print (df)
#df.pivot_table(index=['deid','admit_day'], columns='risk_factor').swaplevel(axis=1).sort_index(1)
#df.pivot(index=['deid','admit_day'], columns='risk_factor', values='result')
#df.pivot(index='risk_factor', columns=['deid','admit_day'], values='result')
#df.set_index(['deid','admit_day','risk_factor']).unstack(level=-1)
#df2 = df.set_index(['deid','admit_day','risk_factor']).unstack(level=-1)
#df2 = df.pivot_table(index=['deid','admit_day'], columns='risk_factor', aggfunc='first')
df2 = df.pivot_table(index=['deid','admit_day'], columns='risk_factor', aggfunc='first')
#df2 = df2.unstack(level=-1)
print (list(df2.columns.values))
df2.columns = [" ".join(('vital',j)) for i,j in df2.columns]
df2.reset_index()
print (list(df2.columns.values))
#df2 = df2.drop('result',0)
#print (df2)

# save csv
df2.to_csv('./csv_data/vitals_extract_GT_new3.csv')