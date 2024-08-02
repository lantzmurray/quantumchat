import streamlit as st
import cohere
import os
import textwrap
import json
import random
import time

# Set up Cohere client
#st.text_input("Cohere APIKey", type="cohere_api_key", key="password")
# Get your API key: https://dashboard.cohere.com/api-keys

st.title("Lantz Murray - 🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
tab1, tab2, tab3 = st.tabs(["Cohere API Key", "Chat", "About"])

with tab1:
    st.header("Cohere API Key")
    st.write("Enter your *Cohere! API key* below.")
    st.write(" *If you don't have an API key go to :* https://cohere.com to sign up for one")
    API_KEY = st.text_input('Cohere! API KEY', key='cohere_api_key', type= "password")
    
    ##st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
with tab2:
    st.header("Chat and Learn")
    
    co = cohere.Client
    (API_KEY,
     # This is your trial API key
    ) 
    stream = co.chat_stream( 
        model='command-r-plus',
        message='<YOUR MESSAGE HERE>',
        temperature=0.3,
        chat_history=[],
        prompt_truncation='AUTO',
        connectors=[{"id":"web-search"}]
        ) 

    

    
    
    
    #st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("About Lantz Murray")
