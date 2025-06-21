from openai import OpenAI
import streamlit as st

# 제목
st.title("수종의 chatGPT")

# 비밀번호 확인
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 비밀번호 입력 UI
if not st.session_state.authenticated:
    password = st.text_input("비밀번호를 입력하세요:", type="password")
    if password and password == st.secrets.get("password"):
        st.session_state.authenticated = True
        st.experimental_rerun()
    elif password:
        st.error("비밀번호가 올바르지 않습니다.")
    st.stop()

# 인증 완료 후 실행되는 본 기능
client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4.1"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
