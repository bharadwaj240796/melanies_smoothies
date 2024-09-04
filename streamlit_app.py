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
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()
ingredients_list = st.multiselect('Choose upto 5 ingredients',my_dataframe,max_selections =5)
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
import requests

if ingredients_list:

    ingredients_string = ''
    
    for fruit_choosen in ingredients_list:
        ingredients_string = ingredients_string+' '+fruit_choosen
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_choosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    st.write(ingredients_string)

    my_insert_statement = """insert into smoothies.public.orders(ingredients,name_on_order)
                values('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    st.write(my_insert_statement)
    time_to_insert = st.button('Submit Oder')
    if time_to_insert:
        session.sql(my_insert_statement).collect()
        st.success("Your Smoothie is ordered!"+name_on_order+".", icon="✅")
