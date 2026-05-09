import json

import pandas as pd
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt
df1 = pd.read_excel('C:/Users/user/Desktop/online_retail_analysis/data/online_retail_II.xlsx', sheet_name=0)
df2 = pd.read_excel('C:/Users/user/Desktop/online_retail_analysis/data/online_retail_II.xlsx', sheet_name=1)

df = pd.concat([df1, df2])

#cleaning
df = df[df['Customer ID'].notna()]
df['Description'] = df['Description'].fillna('Unknown')
df = df[df['Quantity'] > 0]
df['total_price'] = df['Price'] * df['Quantity']





#Customer analysis
customer_report = df.groupby(['Customer ID']).agg(
    purchased = ('total_price', 'sum'),
    item_sold = ('Quantity', 'sum'),
    orders = ('Invoice', "nunique")
)
customer_report['avg_order_value'] = customer_report['purchased'] / customer_report['orders']
best_customer = customer_report['purchased'].idxmax()
customer_report = customer_report.sort_values('purchased', ascending=False)
customer_report = customer_report.reset_index()
customer_report.to_csv('customer_summary_report.csv')

#bar chart
top_10 = customer_report.sort_values('purchased', ascending=False).head(10)
top_10['rank'] = range(1,len(top_10) + 1)
plt.barh(top_10['rank'], top_10['purchased'])
plt.xlabel('Amount Purchased')
plt.ylabel('Top customers (rank)')
plt.title('Top 10 Customers by Purchase')
plt.gca().invert_yaxis()
plt.savefig('Top_Customers_Purchase.png')

#histogram
plt.figure()
plt.hist( customer_report['avg_order_value'], bins='auto',edgecolor='black')
plt.yscale('log')
plt.title('Distribution of AOV')
plt.xlabel('order_value')
plt.ylabel('Number of Customers')
plt.savefig('Top_Customers_AOV.png')




#Country analysis
top_country = df.groupby(['Country']).agg(
    total_price = ('total_price', 'sum'),
    customers = ('Customer ID', 'nunique')
)
top_country['avg_country_value'] = top_country['total_price'] / top_country['customers']
best_country = top_country['total_price'].idxmax()
top_country = top_country.sort_values(by='total_price', ascending=False)

top_country = top_country.reset_index()
top_country.to_csv('country_summary_report.csv')

#Country plot
plt.figure()
top10_country = top_country.sort_values('total_price', ascending=False).head(10)
plt.barh(top10_country['Country'], top10_country['total_price'])
plt.title('Top 10 Country by purchased')
plt.xlabel('Total Price')
plt.ylabel('Top countries')
plt.gca().invert_yaxis()
plt.savefig('Top_countries_Purchase.png')





#Time analysis
df['invoice_month'] = df['InvoiceDate'].dt.to_period("M")
time_sales_report = df.groupby('invoice_month')['total_price'].sum()
time_sales_report.to_csv('monthly_sales_report.csv')

#time_plot
plt.figure()
plt.plot(time_sales_report.index.astype(str), time_sales_report.values)
plt.xlabel('Invoice Month')
plt.ylabel('Total Price')
plt.title('Total Sales by Invoice Month')
plt.savefig('monthly_sales_report.png')




#key metrics
best_product = df['Description'].value_counts().idxmax()
total_revenue = df['total_price'].sum()


#average order value
total_orders = df['Invoice'].nunique()
aov =round(total_revenue / total_orders , 2)

#units per transaction
upt = round(df['Quantity'].sum() / total_orders,2)

key_metrics = dict()
key_metrics['AOV'] = aov
key_metrics['UPT'] = upt
key_metrics['Total Revenue'] = total_revenue
key_metrics['Best Product'] = best_product
key_metrics['Total Orders'] = total_orders

with open('key_metrics.json', 'w') as f:
    json.dump(key_metrics, f, indent=4)



