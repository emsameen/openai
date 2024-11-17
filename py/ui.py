import streamlit as st
from io import StringIO

st.set_page_config(page_title="SW-Factory Assistant")
st.write("# Test Automation Assistant")
input = st.text_input("## Enter a prompt for the requirements/tests ?", value="enter here")
st.write(f"## You entered: {input}")

with st.form("my_form"):
   st.write("Inside the form")
   tempreture = st.slider('Pick a tempreture', 1, 10)
   color = st.selectbox('Pick a color', ['red','orange','green','blue','violet'])
   st.form_submit_button('Submit my picks')

# This is outside the form
st.write(tempreture)
st.write(color)


st.text_area(label="Enter prompt: ", value="this is default values")
req_file = st.file_uploader("Upload requirements file")
req_str = StringIO(req_file.getvalue().decode("utf-8"))
st.write(req_str)