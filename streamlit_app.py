# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)
cnx = st.connection("snowflake")
session = cnx.session()
name_on_smoothie = st.text_input('Name on smoothie:')
st.write(f"Name:{name_on_smoothie}")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose upto 5 ingredients', my_dataframe,max_selections=5)
ingredients_str=''
if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_str+=fruit_chosen+' '
        
    # my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            # values ('""" + ingredients_str ++ ','+name_on_smoothie+"""')"""
    my_insert_stmt = "insert into smoothies.public.orders(ingredients,name_on_order) values ('"+ingredients_str+"','"+name_on_smoothie+"')";
    st.write(my_insert_stmt)
    
    submit_order = st.button("Submit Order")
    if submit_order:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered,{name_on_smoothie}!', icon="✅")
