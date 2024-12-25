import streamlit as st
from openai import OpenAI

# Thêm logo ở trên cùng, căn giữa.
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/nhuannguyen1/chatbotnew1/refs/heads/main/logo.png" alt="Logo" style="width: 50px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Căn chỉnh tiêu đề vào giữa
st.markdown(
    """
    <h1 style="text-align: center;">Xin Chào, Tôi Là Trợ Lý Tư Vấn Pyan</h1>
    """,
    unsafe_allow_html=True
)

# Lấy OpenAI API key từ `st.secrets`.
openai_api_key = st.secrets.get("OPENAI_API_KEY")

# Tạo OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Khởi tạo lời nhắn "system" để định hình hành vi mô hình.
INITIAL_SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "Bạn là một trợ lý ảo thông minh, có thể trả lời câu hỏi của người dùng một cách chính xác, thân thiện, và hữu ích. "
        "Ngoài ra, bạn có thể đóng vai trò tư vấn viên chuyên nghiệp để hỗ trợ những câu hỏi phức tạp hoặc có tính chuyên môn. "
        "Hãy luôn lịch sự và cung cấp thông tin rõ ràng."
    ),
}

# Khởi tạo lời nhắn ví dụ từ vai trò "assistant".
INITIAL_ASSISTANT_MESSAGE = {
    "role": "assistant",
    "content": (
        "Chào bạn! Tôi là trợ lý Pyan. Tôi ở đây để giúp bạn với mọi thắc mắc hoặc yêu cầu của bạn. "
        "Hãy cho tôi biết bạn cần hỗ trợ gì nhé!"
    ),
}

# Khởi tạo lời nhắn ví dụ từ vai trò "user".
INITIAL_USER_MESSAGE = {
    "role": "user",
    "content": (
        "Xin chào trợ lý Pyan! Tôi muốn tìm hiểu thêm về cách sử dụng dịch vụ của bạn. "
        "Bạn có thể giúp tôi được không?"
    ),
}

# Tạo một biến trạng thái session để lưu trữ các tin nhắn nếu chưa tồn tại.
if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_ASSISTANT_MESSAGE]

# Hiển thị các tin nhắn hiện tại bằng `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Tạo ô nhập liệu cho người dùng.
if prompt := st.chat_input("Anh em nhập câu hỏi vào đây ?"):

    # Lưu trữ và hiển thị tin nhắn của người dùng.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tạo phản hồi từ API OpenAI.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Hiển thị và lưu phản hồi của trợ lý.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
