import pandas as pd
# import time
# from memory_profiler import memory_usage


# Sample data
# df = pd.read_excel('../data/data_for_main_table.xlsx')
df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx')
agg_df = df.groupby('Project Name').agg({'Prelims':'sum', 'Measured Works':'sum', 'ToComplete Costs':'sum'})
# agg_df_t = agg_df.transpose()
agg_df.reset_index(inplace=True)
# Checking which approach is faster
# start_time = time.time()
# start_mem = memory_usage()[0]
# last_date_df = pd.read_excel('../data/data_for_main_table.xlsx', sheet_name='LastStatePerProject_VIEW')
last_date_df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx', sheet_name='LastStatePerProject_VIEW')
# last_date_idx = df.groupby('Project Name')['Date'].idxmax()
# last_date_df = df.loc[last_date_idx].reset_index(drop=True)
last_date_df = last_date_df.drop(['Date'], axis='columns')
# end_mem = memory_usage()[0]
# end_time = time.time()
# print(f'\n\n\nFinished in {end_time - start_time} and used {end_mem - start_mem}')
# Done checking