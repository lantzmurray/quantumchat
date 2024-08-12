import streamlit as st
import cohere

# Streamlit App Title
st.title("Quantum Learning Assistant - by Lantz Murray")
st.write(
    "Welcome to your Quantum Computing learning companion! This app is designed to assist you in understanding and mastering the concepts of quantum computing and Qiskit."
)
tab1, tab2, tab3 = st.tabs(["Cohere API Key", "Chat and Learn", "About"])

with tab1:
    st.header("Cohere API Key")
    st.write("Enter your *Cohere API key* below to get started.")
    st.write(" *If you don't have an API key, you can sign up at:* [cohere.com](https://cohere.com)")
    API_KEY = st.text_input('Cohere API Key', key='cohere_api_key', type="password")
    
with tab2:
    st.header("Chat and Learn")

    if API_KEY:
        co = cohere.Client(API_KEY)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Moving the chat input to the bottom of the tab
        prompt = st.chat_input("What Quantum material would you like to learn?")

        if prompt:
            # Display the user message in the chat message container
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            # Stream assistant response from Cohere API
            with chat_container:
                with st.chat_message("assistant"):
                    # Prepare the chat history for the API
                    chat_history = [
                        {"role": "User", "message": m["content"]} if m["role"] == "user" else {"role": "Chatbot", "message": m["content"]}
                        for m in st.session_state.messages
                    ]

                    # Stream response from Cohere API
                    with st.spinner("Assistant is typing..."):
                        full_response = ""
                        source = ""
                        stream = co.chat_stream(
                            model='command-r-plus',
                            message=prompt,
                            temperature=0.3,
                            chat_history=chat_history,
                            preamble="You are an AI assistant specialized in helping users learn concepts of quantum computing and Qiskit. "
    "You have web search capabilities enabled through a Retrieval-Augmented Generation (RAG) model using Cohere Command R+, allowing you to retrieve "
    "relevant information from external sources to assist in generating responses. Provide thorough and helpful explanations "
    "and guide users through learning these topics.",
                            prompt_truncation='AUTO',
                            connectors=[{"id":"web-search"}]
                        )

                        for event in stream:
                            if event.event_type == "text-generation":
                                full_response += event.text
                            elif event.event_type == "citation" and "source" in event:  # Assuming citations come with a "source" field
                                source = event.source

                        # Once the full response is received, update the UI
                        full_response = full_response.strip()
                        
                        if source:
                            full_response += f"\n\n*Source: {source}*"

                        st.markdown(full_response)

                        # Add the full assistant response to message history
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        st.write("Please enter your Cohere API key in the first tab.")

with tab3:
    st.header("About Quantum Learning Assistant")
    
    st.subheader("Overview")
    st.write(
        "Quantum Learning Assistant is an AI-powered educational tool designed to help users explore and understand the complex "
        "world of quantum computing and Qiskit. Developed by Lantz Murray, this application leverages the Cohere API's powerful "
        "language models to provide accurate, context-aware responses to your questions, facilitating a personalized learning experience."
    )
    
    st.subheader("Features")
    st.write(
        """
        - **AI-Powered Learning:** Utilizing state-of-the-art natural language processing (NLP) models, this assistant can answer a wide range of questions related to quantum computing, offering detailed explanations and guidance tailored to your needs.
        - **Retrieval-Augmented Generation (RAG):** This app is equipped with web search capabilities, enabling it to retrieve and incorporate the latest and most relevant information from external sources. This ensures that the responses you receive are both accurate and up-to-date.
        - **User-Friendly Interface:** The app is designed with simplicity in mind, providing an intuitive interface that allows users to focus on learning without getting bogged down by technical complexities.
        - **Real-Time Interaction:** Engage in real-time conversations with the assistant, asking questions and receiving immediate, informative responses that help you build your knowledge of quantum computing incrementally.
        - **Extensive Knowledge Base:** While the assistant has powerful retrieval capabilities, it also draws upon a vast amount of pre-existing knowledge, making it a reliable resource even when offline retrieval is not possible.
        """
    )
    
    st.subheader("How It Works")
    st.write(
        "Quantum Learning Assistant operates by integrating Cohere's advanced language models with a Retrieval-Augmented Generation (RAG) system. "
        "When you ask a question, the app first consults its internal knowledge base, built on extensive training data related to quantum computing and Qiskit. "
        "If needed, it then reaches out to external sources via web search to find the most relevant and up-to-date information. The retrieved content is "
        "then processed by the language model, which generates a coherent and contextually appropriate response tailored to your query."
    )
    
    st.subheader("Who Should Use This App?")
    st.write(
        "This app is perfect for anyone interested in quantum computing, whether you're a beginner just starting out or an advanced learner looking to deepen your understanding. "
        "Educators can also use this tool to supplement their teaching materials, providing students with a responsive and interactive learning assistant."
    )
    
    st.subheader("Developer Information")
    st.write(
        "Quantum Learning Assistant was developed by Lantz Murray, a passionate developer with a deep interest in AI and quantum computing. "
        "The app is open-source and contributions are welcome. You can find the project's repository on GitHub: "
        "[Quantum Learning Assistant on GitHub](https://github.com/lantzmurray/quantumchat)."
    )
    
    st.subheader("License")
    st.write(
        "This project is licensed under the MIT License, allowing you to freely use, modify, and distribute the software. For more details, "
        "please refer to the [LICENSE](https://github.com/lantzmurray/quantumchat/blob/main/LICENSE) file in the GitHub repository."
    )
