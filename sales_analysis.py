import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

#load csv

df = pd.read_csv("sales.csv")
print("Dataset loaded:")
print (df.head())

#create sql db

conn = sqlite3.connect("sales.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

#total sales
total_sales = pd.read_sql_query("SELECT SUM(`Total`) AS Total_Sales FROM sales;", conn)
print ("\nTotal Sales:")
print(total_sales)

#top5

top_products = pd.read_sql_query("""
 SELECT `Product line`, SUM(`Total`) AS Total_Sales
 FROM sales
 GROUP BY `Product line`
 ORDER BY Total_Sales DESC
 LIMIT 5;
 """, conn)        

print("\nTop 5 Product lines by Sales:")  
print (top_products) 

# Monthly Sales Trend
monthly_sales = pd.read_sql_query("""
SELECT substr(Date,1,7) AS Month, SUM(`Total`) AS Total_Sales
FROM sales
GROUP BY Month
ORDER BY Month;
""", conn)
print("\nMonthly Sales Trend:")
print(monthly_sales)

# Sales by Branch
region_sales = pd.read_sql_query("""
SELECT Branch, SUM(`Total`) AS Total_Sales
FROM sales
GROUP BY Branch
ORDER BY Total_Sales DESC;
""", conn)
print("\nSales by Branch:")
print(region_sales)

# Visualizations
sns.barplot(data=top_products, x='Product line', y='Total_Sales')
plt.title("Top 5 Product Lines by Sales")
plt.xticks(rotation=45)
plt.show()

sns.lineplot(data=monthly_sales, x='Month', y='Total_Sales', marker='o')
plt.title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.show()

plt.pie(region_sales['Total_Sales'], labels=region_sales['Branch'], autopct='%1.1f%%')
plt.title("Sales by Branch")
plt.show()