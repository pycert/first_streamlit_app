import pandas as pd
import requests
import streamlit as st
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

st.header("Fruityvice Fruit Advice!")

try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error('Please select a fruit to get information.')
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error()

st.stop()

st.header("The fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

    if st.button('Get fruit load list'):
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        my_data_rows = get_fruit_load_list()
        st.dataframe(my_data_rows)

add_my_fruit = st.text_input('What fruit would you like to add?')
st.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values('from Streamlit');")
