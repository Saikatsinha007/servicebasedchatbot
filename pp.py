import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Set up Streamlit page
st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("💬 AI Chatbot")
st.caption("Your friendly AI assistant for simple explanations!")

# Initialize the model
model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434/")

# Define system message
system_message = SystemMessagePromptTemplate.from_template(
    "You are a helpful AI Assistant. You work as a teacher for 5th-grade students. You explain things in short and brief."
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to generate response
def generate_response(chat_history):
    chat_template = ChatPromptTemplate.from_messages(chat_history)
    chain = chat_template | model | StrOutputParser()
    response = chain.invoke({})
    return response

# Sidebar for input
with st.sidebar:
    st.header("📝 Ask a Question")
    user_input = st.text_area("Type your question here...")
    if st.button("Submit") and user_input:
        st.session_state.chat_history.append({"user": user_input, "assistant": "Thinking..."})

# Process response
if st.session_state.chat_history and st.session_state.chat_history[-1]["assistant"] == "Thinking...":
    chat_history = [system_message]
    for chat in st.session_state.chat_history:
        chat_history.append(HumanMessagePromptTemplate.from_template(chat["user"]))
        if chat["assistant"] != "Thinking...":
            chat_history.append(AIMessagePromptTemplate.from_template(chat["assistant"]))
    
    response = generate_response(chat_history)
    st.session_state.chat_history[-1]["assistant"] = response

# Display conversation history
st.write("## 📜 Conversation History")
for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**👤 You:** {chat['user']}")
    st.markdown(f"**🤖 AI:** {chat['assistant']}")
    st.divider()
