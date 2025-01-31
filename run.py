import pandas as pd
import streamlit as st
from main import product

st.title("ShopSort")

product_name = st.text_input("Enter product name: ")


if product_name:
    pd_data = product(product_name)
    df = pd.DataFrame(pd_data)
    

    #Starts index from 1 and changes the column's name to 'No.'
    df.index = df.index + 1
    df.index.name = 'No.'

    #make the dataframe links clickable
    df['Platform link'] = df['Platform link'].apply(lambda x: f'<a href="{x}" target="_blank">Click here</a>')

    #using HTML and CSS to change the appearance of the table
    html_table = df.to_html(escape=False, index=False)

    #to fit container width
    st.markdown("""
    <style>
        .dataframe {
            width: 100% !important;
            overflow-x: auto;  /* Allows horizontal scrolling if needed */
        }
        table {
            width: 100% !important;
            table-layout: fixed;
        }
        th, td {
            text-align: left;
            padding: 8px;
            white-space: nowrap;  /* Prevent text from breaking into multiple lines */
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the HTML table with clickable links
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.warning("Enter product name")
# except:
#     st.warning("Error occurred. Please try again!")