import json
import os

import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Doc QA Bot", page_icon="📚", layout="centered")
st.title("📚 Doc QA Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

with st.sidebar:
    if st.button("새 대화 시작", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

    if st.session_state.session_id:
        st.caption(f"session: `{st.session_state.session_id[:8]}...`")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("출처"):
                for src in msg["sources"]:
                    st.write(src)

if prompt := st.chat_input("질문을 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    state: dict = {}

    def token_stream():
        with requests.post(
            f"{API_BASE}/query/stream",
            json={"question": prompt, "session_id": st.session_state.session_id},
            stream=True,
            timeout=120,
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line:
                    continue
                if line.startswith(b"data: "):
                    event = json.loads(line[6:])
                    if event["type"] == "token":
                        yield event["data"]
                    elif event["type"] == "sources":
                        state["sources"] = event["data"]
                    elif event["type"] == "done":
                        state["session_id"] = event["session_id"]

    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(token_stream())
            sources = state.get("sources", [])
            if sources:
                with st.expander("출처"):
                    for src in sources:
                        st.write(src)
        except requests.exceptions.ConnectionError:
            st.error("API 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
            st.stop()
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.stop()

    st.session_state.session_id = state.get("session_id", st.session_state.session_id)
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": state.get("sources", []),
    })
