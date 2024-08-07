import streamlit as st
import numpy as numpy
import pandas as pd


def load_data():
    file = 'bakerysales.csv'
    df = pd.read_csv(file)
    df.rename(columns={'Unnamed: 0': 'id',
                       'article':'product', 
                       'Quantity':'quantity'}, 
                       inplace=True)
    df.unit_price = df.unit_price.str.replace(",",".").str.replace("€","").str.strip()
    df.unit_price = df.unit_price.astype('float')
    #calculate sales
    df['sales'] = df.quantity * df.unit_price
    # drop columns with zero sales
    df.drop(df[df.sales == 0].index, inplace=True)
    # convert date column to date format 
    df['date'] = pd.to_datetime(df.date)
    return df

# load the dataset
df = load_data()
 
# app title
st.title("Bakery Sales App")
# display the table
# st.dataframe(df.head(50))

# select the display specific products
# add filter

products = df['product'].unique()
selected_products = st.sidebar.multiselect(
                     "Choose Product",
                      products,
                      [products[0],
                      products[2]
                      ]) 
filtered_table = df[df['product'].isin(selected_products)]

# display metrics
# total sale = 0
if len(filtered_table) > 0:
    total_sales = filtered_table['sales'].sum()
else:
    total_sales = df.sales.sum()

total_qty = df.quantity.sum()
total_no__transactions = df.id.count()

st.subheader("calculations")
col1, col2, col3 = st.columns(3)

col1.metric("no of Transactions", total_no__transactions)
col2.metric("Total Quantity", total_qty)
col3.metric("Total Sales", total_sales)
            
# end of metrics

# display the filtered table
# specific columns 
st.dataframe(filtered_table[["date","product",
                             "quantity","unit_price",
                            "sales"]])

# bar chart
try:
    st.write("## Total sale of selected product")
    bar1 = filtered_table.groupby(['product'])['sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1)
except ValueError as e:
    st.error(
        """ Error """ % e.reason
    )    

