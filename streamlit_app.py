import streamlit as st
import openai

# Show title and description.
st.title("Trợ lý tư vấn Pyan")
st.write("Tôi là Nhuần, đến từ PYAN.")

# Lấy OpenAI API key từ `st.secrets`.
openai_api_key = st.secrets.get("OPENAI_API_KEY")

if not openai_api_key:
    st.error("API Key không tồn tại trong `st.secrets`. Vui lòng cấu hình `secrets.toml`.")
else:
    # Set the OpenAI API key.
    openai.api_key = openai_api_key

    # Tạo biến trạng thái session để lưu các tin nhắn của cuộc trò chuyện.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Hiển thị các tin nhắn đã lưu trong trạng thái session.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Tạo trường nhập liệu để người dùng nhập tin nhắn.
    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):

        # Lưu và hiển thị tin nhắn của người dùng.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gửi yêu cầu đến OpenAI API để tạo phản hồi.
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )

            # Trích xuất phản hồi từ API và hiển thị.
            assistant_message = response["choices"][0]["message"]["content"]
            with st.chat_message("assistant"):
                st.markdown(assistant_message)

            # Lưu phản hồi vào trạng thái session.
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        except Exception as e:
            st.error(f"Đã xảy ra lỗi khi gọi OpenAI API: {e}")
