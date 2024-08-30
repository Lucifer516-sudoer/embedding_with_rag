# import streamlit as st
# import requests
# import json

# # Set page config
# st.set_page_config(page_title="AI Chat", page_icon="✨", layout="wide")

# # Custom CSS to match the dark theme and improve layout
# st.markdown(
#     """
# <style>
#     .stApp {
#         background-color: #1E1E1E;
#         color: #FFFFFF;
#     }
#     .stSidebar {
#         background-color: #252526;
#     }
#     .stTextInput > div > div > input {
#         background-color: #3C3C3C;
#         color: #FFFFFF;
#         border: 1px solid #565656;
#     }
#     .stButton > button {
#         background-color: #565656;
#         color: #FFFFFF;
#     }
#     .stSelectbox > div > div > select {
#         background-color: #3C3C3C;
#         color: #FFFFFF;
#     }
#     .chat-message {
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 1rem;
#         display: flex;
#         align-items: flex-start;
#     }
#     .chat-message.user {
#         background-color: #2D2D2D;
#     }
#     .chat-message.bot {
#         background-color: #3D3D3D;
#     }
#     .chat-message .avatar {
#         width: 40px;
#         height: 40px;
#         border-radius: 50%;
#         object-fit: cover;
#         margin-right: 1rem;
#     }
#     .chat-message .message {
#         flex-grow: 1;
#     }
#     .stChatInputContainer {
#         padding-bottom: 5rem;
#     }
#     .stChatInput {
#         background-color: #3C3C3C;
#         border: 1px solid #565656;
#         border-radius: 20px;
#     }
#     .welcome-message {
#         text-align: center;
#         padding: 2rem;
#         background-color: #3D3D3D;
#         border-radius: 0.5rem;
#         margin-bottom: 2rem;
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Sidebar
# with st.sidebar:
#     st.title("Chat Options")
#     endpoint = st.selectbox("Select Endpoint", ["/ai", "/ask_pdf"])

#     st.subheader("Upload a PDF")
#     uploaded_file = st.file_uploader(
#         "Drag and drop file here", type="pdf", help="Limit 200MB per file • PDF"
#     )

#     if uploaded_file:
#         with st.spinner("Uploading and processing PDF..."):
#             try:
#                 files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
#                 response = requests.post("http://localhost:8080/pdf", files=files)
#                 response.raise_for_status()
#                 st.success("PDF uploaded and processed successfully!")
#             except requests.exceptions.RequestException as e:
#                 st.error(f"An error occurred while uploading the PDF: {e}")

# # Main chat interface
# st.title("AI Chat")

# # Welcome message
# if not st.session_state.messages:
#     st.markdown(
#         """
#     <div class="welcome-message">
#         <h2>Welcome to AI Chat!</h2>
#         <p>Start a conversation by typing your message in the chat box below.</p>
#         <p>You can ask questions, request information, or engage in a discussion on various topics.</p>
#     </div>
#     """,
#         unsafe_allow_html=True,
#     )

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# # Chat input
# user_input = st.chat_input("Type your message here...")

# if user_input:
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.write(user_input)

#     # Send request to API
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         try:
#             with st.spinner("Thinking..."):
#                 response = requests.post(
#                     f"http://localhost:8080{endpoint}",
#                     json={"query": user_input},
#                     stream=True,
#                 )
#                 response.raise_for_status()

#                 # Stream the response
#                 for chunk in response.iter_content(chunk_size=1):
#                     if chunk:
#                         full_response += chunk.decode("utf-8")
#                         message_placeholder.markdown(full_response + "▌")
#                 message_placeholder.markdown(full_response)

#             # Add assistant message to chat history
#             st.session_state.messages.append(
#                 {"role": "assistant", "content": full_response}
#             )

#         except requests.exceptions.RequestException as e:
#             st.error(f"An error occurred: {e}")

# # Remove the run instructions
# # if __name__ == "__main__":
# #     st.write("To run this app, save it as 'app.py' and run 'streamlit run app.py' in your terminal.")

# import streamlit as st
# import requests
# import json
# import httpx

# async_client = httpx.AsyncClient(
#     timeout=None,
# )
# # Set page config
# # st.set_page_config(page_title="AI Chat", page_icon="✨", layout="wide")
# st.set_page_config(page_title="VSBEC", page_icon="icons/revolvo.png", layout="wide")

# # Custom CSS (keeping the previous styling)
# st.markdown(
#     """
# <style>
#     .stApp {
#         background-color: #1E1E1E;
#         color: #FFFFFF;
#     }
#     .stSidebar {
#         background-color: #252526;
#     }
#     .stTextInput > div > div > input {
#         background-color: #3C3C3C;
#         color: #FFFFFF;
#         border: 1px solid #565656;
#     }
#     .stButton > button {
#         background-color: #565656;
#         color: #FFFFFF;
#     }
#     .stSelectbox > div > div > select {
#         background-color: #3C3C3C;
#         color: #FFFFFF;
#     }
#     .chat-message {
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 1rem;
#         display: flex;
#         align-items: flex-start;
#     }
#     .chat-message.user {
#         background-color: #2D2D2D;
#     }
#     .chat-message.bot {
#         background-color: #3D3D3D;
#     }
#     .chat-message .avatar {
#         width: 40px;
#         height: 40px;
#         border-radius: 50%;
#         object-fit: cover;
#         margin-right: 1rem;
#     }
#     .chat-message .message {
#         flex-grow: 1;
#     }
#     .stChatInputContainer {
#         padding-bottom: 5rem;
#     }
#     .stChatInput {
#         background-color: #3C3C3C;
#         border: 1px solid #565656;
#         // border-radius: 20px;
#     }
#     .welcome-message {
#         text-align: center;
#         padding: 2rem;
#         background-color: #3D3D3D;
#         border-radius: 0.5rem;
#         margin-bottom: 2rem;
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Sidebar
# with st.sidebar:
#     st.title("Chat Options")
#     endpoint = st.selectbox("Select Endpoint", ["/ai", "/ask_pdf"])

#     st.subheader("Upload a PDF")
#     uploaded_file = st.file_uploader(
#         "Drag and drop file here", type="pdf", help="Limit 200MB per file • PDF"
#     )

#     if uploaded_file:
#         try:
#             files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
#             response = requests.post("http://localhost:8080/pdf", files=files)
#             response.raise_for_status()

#             st.success("PDF uploaded and processed successfully!")
#         except requests.exceptions.RequestException as e:
#             st.error(f"An error occurred while uploading the PDF: {e}")

# # Main chat interface
# st.title("AI Chat")

# # Welcome message
# if not st.session_state.messages:
#     st.markdown(
#         """
#     <div class="welcome-message">
#         <h2>Welcome toRevolvo!</h2>
#         <p>Start a conversation by typing your message in the chat box below.</p>
#         <p>You can ask questions, request information, or engage in a discussion on various topics.</p>
#     </div>
#     """,
#         unsafe_allow_html=True,
#     )

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# # Chat input
# user_input = st.chat_input("Type your message here...")

# if user_input:
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.write(user_input)

#     # Send request to API and stream the response
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         try:
#             with requests.post(
#                 f"http://localhost:8080{endpoint}",
#                 json={"query": user_input},
#                 stream=True,
#             ) as response:
#                 response.raise_for_status()
#                 for chunk in response.iter_content(chunk_size=1):
#                     if chunk:
#                         full_response += chunk.decode("utf-8")
#                         message_placeholder.markdown(full_response + "▌")
#             message_placeholder.markdown(full_response)

#             # Add assistant message to chat history
#             st.session_state.messages.append(
#                 {"role": "assistant", "content": full_response}
#             )

#         except requests.exceptions.RequestException as e:
#             st.error(f"An error occurred: {e}")
import streamlit as st
import requests
import json

# Set page config
st.set_page_config(
    page_title="VSB Engineering College", page_icon="icons/revolvo.png", layout="wide"
)


# Custom CSS to match the dark theme and improve layout
st.markdown(
    """
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stSidebar {
        background-color: #252526;
    }
    .stTextInput > div > div > input {
        background-color: #3C3C3C;
        color: #FFFFFF;
        border: 1px solid #565656;
    }
    .stButton > button {
        background-color: #565656;
        color: #FFFFFF;
    }
    .stSelectbox > div > div > select {
        background-color: #3C3C3C;
        color: #FFFFFF;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #2D2D2D;
    }
    .chat-message.bot {
        background-color: #3D3D3D;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex-grow: 1;
    }
    .stChatInputContainer {
        padding-bottom: 5rem;
    }
    .stChatInput {
        background-color: #3C3C3C;
        border: 1px solid #565656;
        // border-radius: 20px;
    }
    .welcome-message {
        text-align: center;
        padding: 2rem;
        background-color: #3D3D3D;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("Chat Options")
    endpoint = st.selectbox("Select Endpoint", ["/ai", "/ask_pdf"])

    st.subheader("Upload a PDF")
    uploaded_file = st.file_uploader(
        "Drag and drop file here", type="pdf", help="Limit 200MB per file • PDF"
    )

    if uploaded_file:
        with st.spinner("Uploading and processing PDF..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post("http://localhost:8080/pdf", files=files)
                response.raise_for_status()
                st.success("PDF uploaded and processed successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while uploading the PDF: {e}")

# Main chat interface
st.title("Revolvo")

# Welcome message
if not st.session_state.messages:
    st.markdown(
        """
    <div class="welcome-message">
        <h2>Welcome to Revolvo!</h2>
        <p>Start a conversation by typing your message in the chat box below.</p>
        <p>You can ask questions, request information, or engage in a discussion on various topics.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Send request to API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"http://localhost:8080{endpoint}",
                    json={"query": user_input},
                    stream=True,
                )
                response.raise_for_status()

                # Stream the response
                for chunk in response.iter_content(chunk_size=1):
                    if chunk:
                        full_response += chunk.decode("utf-8")
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

            # Add assistant message to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

# Remove the run instructions
# if __name__ == "__main__":
#     st.write("To run this app, save it as 'app.py' and run 'streamlit run app.py' in your terminal.")
