Use Python 3.12

3.12


AWS Shell Script

dmgdev

US East (N. Virginia) [us-east-1]

python $(System.DefaultWorkingDirectory)/consumer/dwsqlexec.py

copy into library_card_catalog.public.nested_ingest_json
from '@UTIL_DB.PUBLIC.MY_INTERNAL_STAGE/nutrition_tweets.json'
file_format = social_media_floodgates.public.json_file_format


create file format smoothies.public.two_headerrow_pct_delim
   type = CSV,
   skip_header = 2,   
   field_delimiter = '%',
   trim_space = TRUE
;


# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input('Name On Smoothie:')
st.write('The Name on your Smoothie will be :', name_on_order)

ingredients_list= st.multiselect(
    'choose up to 5 ingredients:'
    , my_dataframe
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered' +  name_on_order +'!' , icon="✅")
