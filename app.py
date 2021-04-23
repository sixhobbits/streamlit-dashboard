import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

DATA_URL = 'https://bern.dwyer.co.za/get_clean'
          

@st.cache
def load_data(nrows=999999999999):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data['date'] = pd.to_datetime(data['date'])
    data['Size'] = data['size'].apply(lambda x: f'{x:.0f} sqm')
    data['Price'] = data['price'].apply(lambda x: f'CHF {x:.0f}')
    return data

st.title('Bern Rental Prices')
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")


st.subheader('Choose filters')

ticks = [float(x)/10 for x in range(10,80,5)]
city_options = list(set(data['city']))

rooms_filter = st.slider('Number of rooms', 1.0, 10.0, (1.0, 10.0), step=0.5)
cities_filter = st.multiselect('Cities', city_options, default=['Bern'])


filtered_data = data[data['num_rooms'].between(rooms_filter[0], rooms_filter[1])]
filtered_data = filtered_data[filtered_data['city'].isin(cities_filter)]

avg = filtered_data['price'].mean()
med = filtered_data['price'].median()
mn = filtered_data['price'].min()
mx = filtered_data['price'].max()

st.markdown(f"### Avg. CHF {avg:.0f} | Med. CHF {med:.0f} | Min. CHF {mn:.0f} | Max CHF {mx:.0f}")

chart = alt.Chart(filtered_data).mark_point().encode(
    x=alt.X('num_rooms', axis=alt.Axis(values=ticks)),
    y='price',
    color='city',
    tooltip=['description', 'post_code', 'Size', 'Price']
).interactive()

st.altair_chart(chart)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(filtered_data)

