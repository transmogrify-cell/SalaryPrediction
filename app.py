import streamlit as st
from predict_pg import show_predict_page
from explore_pg import show_explore_page

# Sidebar navigation
page = st.sidebar.selectbox("Choose a Page", ("Predict", "Explore"))

# Display the appropriate page
if page == "Predict":
    show_predict_page()
else:
    show_explore_page()


# Created by HIMANSHU CHANDELA 
#streamlit run app.py
