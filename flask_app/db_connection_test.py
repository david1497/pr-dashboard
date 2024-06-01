#%%
import pyodbc

#%%
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=laptop-ttip97em\\sqlexpress;DATABASE=platt_reilly;Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users;")
row = cursor.fetchone()
print(row)

# %%
