# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize your own smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruit you want in your custom smoothie.
  """
)

name_on_order=st.text_input('Name on smoothie:')
st.write('Name on your smoothie: ' ,name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_list = st.multiselect(
    "choose upto 5 ingredients to make smoothie",
my_dataframe
)

if ingredients_list:
    #st.write("You selected:", ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
        st.subheader(fruit_chosen +'Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon"+ fruit_chosen)
        #st.text(smoothiefroot_response.json())
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit order')
   #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("""Your Smoothie is ordered! """+ name_on_order +"""
         """)




