import streamlit as st
import cohere

# Streamlit App Title
st.title("Lantz Murray - 🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
tab1, tab2, tab3 = st.tabs(["Cohere API Key", "Chat", "About"])

with tab1:
    st.header("Cohere API Key")
    st.write("Enter your *Cohere! API key* below.")
    st.write(" *If you don't have an API key go to :* https://cohere.com to sign up for one")
    API_KEY = st.text_input('Cohere! API KEY', key='cohere_api_key', type="password")
    
with tab2:
    st.header("Chat and Learn")

    if API_KEY:
        co = cohere.Client(API_KEY)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Moving the chat input to the bottom of the tab
        prompt = st.chat_input("What Quantum material would you like to learn?")

        if prompt:
            # Display the user message in the chat message container
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Stream assistant response from Cohere API
            with st.chat_message("assistant"):
                # Prepare the chat history for the API
                chat_history = [
                    {"role": "User", "message": m["content"]} if m["role"] == "user" else {"role": "Chatbot", "message": m["content"]}
                    for m in st.session_state.messages
                ]

                # Stream response from Cohere API
                with st.spinner("Assistant is typing..."):
                    full_response = ""
                    stream = co.chat_stream(
                        model='command-r-plus',
                        message=prompt,
                        temperature=0.3,
                        chat_history=chat_history,
                        preamble="You are an AI assistant specialized in helping users learn concepts of quantum computing and Qiskit. Provide thorough and helpful explanations and guide them through learning these topics.",
                        prompt_truncation='AUTO',
                        connectors=[{"id":"web-search"}]
                    )

                    for event in stream:
                        if event.event_type == "text-generation":
                            full_response += event.text

                    # Once the full response is received, update the UI
                    full_response = full_response.strip()
                    st.markdown(full_response)

                    # Add the full assistant response to message history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        st.write("Please enter your Cohere API key in the first tab.")

with tab3:
    st.header("About Lantz Murray")
    st.write("This is a simple Streamlit app to demonstrate using the Cohere API.")
