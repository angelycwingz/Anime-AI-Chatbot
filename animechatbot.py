"""
Simple Langchain Streamlit App with Groq
"""

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "ENTER_YOUR_GROQ_API_KEY")
LLM_MODEL = "gemma2-9b-it"

# Page config
st.set_page_config(page_title="Anime AI Chatbot with Groq", page_icon="㊙️")

# Title
st.title("㊙️ Anime AI Chatbot with Groq")
st. markdown("Ask anything about your favorite Anime with Groq's ulra-fast inference!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize LLM
def get_chain(model_name):

    # Initialize the GROQ Model
    llm = init_chat_model(f"groq:{model_name}", temperature=0.7, streaming=True)

    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system","""You are a powerful Anime assistant who is an expert at Anime and Manga. 
         Answer questions clearly and concisely. 
         If someone asks a question outside the scope of Anime remind them 
         you only anwer about Anime or Manga and suggest a random fact related to Anime."""
        ),
        ("user", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()

    return chain

chain = get_chain(LLM_MODEL)

if not chain: 
    st.warning("Something went wrong! Try refreshing the page.")

else:
    # Display the chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    # chat input box
    if question:= st.chat_input("Ask me anything about Anime"):
        # Add message to the session state
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try: 
                # Stream response from Groq
                # Using stream() instead of invoke() because we are streaming in our llm model

                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)

                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Examples
st.markdown("---")
st.markdown("### 😎 Try thes examples:")
col1, col2 = st.columns(2)

with col1:
    st.markdown("- Who is Kakarot?")
    st.markdown("- Why Frieza hate Saiyans")

with col2: 
    st.markdown("- How Uchiha's activated their Sharingan?")
    st.markdown("- Why Itachi Uchiha left his village?")

# Footer
st.markdown("---")
st.markdown("Built with Langchain & Groq | Experience the speed! Like the Yellow Flash⚡ of Konoha")