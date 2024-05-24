# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruit you want to customize your Smoothie!")

name_an_order = st.text_input('Name on Smoothie: ')
st.write('The name on your smoothie will be: ',name_an_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect('choose up to five ingredient'
                                 ,my_dataframe
                                 ,max_selections=5)

if ingredient_list:   
    ingredient_string=''
    
    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_string + """','""" + name_an_order +"""')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        #st.write('query: ',my_insert_stmt)
        
        st.success('Your Smoothie is ordered!', icon="✅")



