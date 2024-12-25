import streamlit as st
from openai import OpenAI



# Thêm logo ở trên cùng, căn giữa.
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://github.com/nhuannguyen1/chatbotnew1/blob/6b935e450254ab561ecdc2a715aaa016f293e0d3/logo.png" alt="Logo" style="width: 150px;">
    </div>
    """,
    unsafe_allow_html=True
)


# Show title and description.
st.title("Trợ lý tư vấn Pyan")

st.write("Tôi là Nhuần Đến từ PYAN")

# Ask user for their OpenAI API key via `st.text_input`.
# Ask user for their OpenAI API key via `st.text_input`.

# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

# Lấy OpenAI API key từ `st.secrets`.
openai_api_key = st.secrets.get("OPENAI_API_KEY")

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Anh em nhập câu hỏi vào đây ?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
