#step9:convert the csv into SQLite

import pandas as pd
import sqlite3

df = pd.read_csv("data/sales_data.csv")

conn = sqlite3.connect("sales.db")

df.to_sql("sales", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully!")

#step10:verify the SQL table(py -3.11 -c "import sqlite3; conn=sqlite3.connect('sales.db'); print(conn.execute('SELECT COUNT(*) FROM sales').fetchone()); conn.close()")
#step11:test an actual SQL calculation(py -3.11 -c "import sqlite3; conn=sqlite3.connect('sales.db'); print(conn.execute('SELECT SUM(Sales) FROM sales').fetchone()); conn.close()")
#step12:test a more useful SQL query(py -3.11 -c "import sqlite3; conn=sqlite3.connect('sales.db'); print(conn.execute('SELECT Product, SUM(Sales) AS TotalSales FROM sales GROUP BY Product ORDER BY TotalSales DESC LIMIT 1').fetchone()); conn.close()")
#step13:important:inspect the table structure(py -3.11 -c "import sqlite3; conn=sqlite3.connect('sales.db'); print(conn.execute('PRAGMA table_info(sales)').fetchall()); conn.close()")