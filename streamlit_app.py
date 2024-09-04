# Import python packages
import streamlit as st

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose your fruits you want in your customize smoothie.
    """
)

name_on_order = st.text_input('Name on smoothie')
st.write('Name on your smoothie will be :',name_on_order)
from snowflake.snowpark.functions import col
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
ingredients_list = st.multiselect('Choose upto 5 ingredients',my_dataframe,max_selections =5)
# st.dataframe(data=my_dataframe, use_container_width=True)
if ingredients_list:

    ingredients_string = ''
    
    for fruit_choosen in ingredients_list:
        ingredients_string = ingredients_string+' '+fruit_choosen
    st.write(ingredients_string)

    my_insert_statement = """insert into smoothies.public.orders(ingredients,name_on_order)
                values('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    st.write(my_insert_statement)
    time_to_insert = st.button('Submit Oder')
    if time_to_insert:
        session.sql(my_insert_statement).collect()
        st.success("Your Smoothie is ordered!"+name_on_order+".", icon="✅")
