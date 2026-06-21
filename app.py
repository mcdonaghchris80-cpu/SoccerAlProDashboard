
import streamlit as st
from dashboard.home import render_home
st.set_page_config(page_title='Soccer AI Pro',layout='wide')
render_home()
