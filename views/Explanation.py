import pandas as pd
import streamlit as st
from datetime import date

st.title('About this project')


#st.subheader('Please Note', divider= 'gray')
st.text('The purpose of this project was to create a Streamlit app that provides information and insights about my record collection and wantlist based on data from my personal Discogs account.')

st.markdown('[Discogs](https://www.discogs.com/) is the main online database and marketplace for all kinds audio recordings, making it the ideal tool for keeping track of your personal music collection and wantlist. With the help of the [Discogs-API](https://python3-discogs-client.readthedocs.io/en/latest/about.html) you can retrieve data regarding your personal account, such as collection and wantlist.')

st.markdown('Based on this, first I extracted data regarding my personal record [collection](https://www.discogs.com/de/user/CarlMenger/collection?header=1) and [wantlist](https://www.discogs.com/wantlist?user=CarlMenger) from Discogs. In the second step, I used this data to build an interactive dashboard using the streamlit library.')


#st.subheader('About this project', divider= 'gray')

#st.text('Note: ')



#search = st.secrets['search']
#st.image(search, caption = 'google search for ichiban', width = 500)
