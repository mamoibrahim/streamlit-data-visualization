import streamlit as st 
import pandas as pd 
import plotly.express as px
import numpy as np
from wordcloud import WordCloud , STOPWORDS
import matplotlib.pyplot as plts


st.set_page_config (
    page_title = 'Dashboard',
    page_icon = '🌿',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

st.title('sentiment analysis of tweets about us airlines ')
st.sidebar.title('sentiment analysis of tweets about us airlines')

st.markdown('this is a dashboard for sentiment analysis of tweets about us airlines')
st.sidebar.markdown('this is a dashboard for sentiment analysis of tweets about us airlines')

#url = "C:\Users\x\Desktop\streamlit-viz\Tweets.csv"

#to not load the data every time the page is refreshed 
st.cache(persist=True)
def load_data():
    data = pd.read_csv('Tweets.csv')
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data 


data = load_data()

st.sidebar.subheader('show random tweet')
ranom_tweet = st.sidebar.radio('sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment== @   ranom_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown('### number of tweets by sentiment')
Select =  st.sidebar.selectbox('vizualisation type', ['histogram', 'pie chart'] , key='1')

sentiment_count = data['airline_sentiment'].value_counts()

if not st.sidebar.checkbox('Hide chart', True) : 
        st.markdown('### NUMBER OF TWEETS BY SENTIMENT')
        if Select == 'histogram':
              fig = px.bar(sentiment_count, x = sentiment_count.index, y = sentiment_count.values , color='count' , height=500)
              st.plotly_chart(fig)
        else:
              fig = px.pie(sentiment_count, values = sentiment_count.values, names = sentiment_count.index)
              st.plotly_chart(fig)  



st.sidebar.subheader('when and where are users tweeting from')
hour = st.sidebar.slider('hour of day', 0, 23 )
modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox('close map', True):
    st.markdown('### tweets locations based on time of day')   
    st.markdown('%i tweets between %i:00 and %i:00'% (len(modified_data) , hour ,( hour+1)%24 ) )
    st.map(modified_data)
    if st.sidebar.checkbox('show raw data', False):
        st.write(modified_data)


st.sidebar.subheader('Breakdown airline tweets by sentiment')
choice = st.sidebar.multiselect(
    'pick airlines',
    ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'),key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig = px.histogram(
        choice_data,
        x='airline',
        y='airline_sentiment',
        histfunc='count',
        color='airline_sentiment',
        facet_col='airline_sentiment',
        labels={'airline_sentiment': 'tweets'},
        height=600,
        width=800
    )
    st.plotly_chart(fig)

st.sidebar.header('Word Cloud')
word_sentiment = st.sidebar.radio(
    'display word cloud for what?',
    ('positive', 'neutral', 'negative')
)

if not st.sidebar.checkbox('close', True, key='3'):
    df = data[data['airline_sentiment'] == word_sentiment]
    text = ' '.join(df['text'])
    processed_text = ' '.join([word for word in text.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black', width=400, height=210).generate(processed_text)
    plts.imshow(wordcloud, interpolation='bilinear')
    plts.axis('off')
    st.pyplot(plts)     