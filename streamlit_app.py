import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title(" My parents new healthy diner")
streamlit.header('Breakfast Menu')
streamlit.text('π₯£ Omega 3 & Blueberry Oatmeal')
streamlit.text('π₯ Kale, Spinach & Rocket Smoothie')
streamlit.text('πHard-Boiled Free-Range Egg')
streamlit.text('π₯π Avocado Toast')
streamlit.header('ππ₯­ Build Your Own Fruit Smoothie π₯π')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list if fruits_selected==[] else my_fruit_list.loc[fruits_selected]


# Display the table on the page.

streamlit.dataframe(fruits_to_show)

def get_fruitvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    streamlit.write('The user entered ', fruit_choice)
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()




def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list;")
    my_cnx.close()
    return my_cur.fetchall()
    
  


streamlit.text("The fruit load contains: ")

if streamlit.button("Get Fruit Load list"):
  my_cnx =  snowflake.connector.connect(
  user= "juracal",
  password= "Mel.Viento16",
  account= "cq44194.ca-central-1.aws",
  warehouse="compute_wh",
  database="pc_rivery_db",
  schema="public"
)
  my_data = get_fruit_load_list()
  streamlit.dataframe(my_data)
 
def insert_row(new_fruit):
  my_cnx =  snowflake.connector.connect(
  user= "juracal",
  password= "Mel.Viento16",
  account= "cq44194.ca-central-1.aws",
  warehouse="compute_wh",
  database="pc_rivery_db",
  schema="public"
)
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit +"')")
    return "Thanks for addding" + new_fruit
  
add_my_fruit = streamlit.text_input("What fruit would you like to add?")

if streamlit.button("Add Fruit to list"):
  my_data = insert_row(add_my_fruit)
  streamlit.text(my_data)
streamlit.stop()

