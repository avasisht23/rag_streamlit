import streamlit as st

from clients.llama_idx import LlamaIndexClient

st.title("Earnings Calls RAG App")
st.info(
    "Check out the full tutorial on this [Github repo](https://github.com/avasisht23/rag_streamlit)!",
    icon="📃",
)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about Company earnings calls!",
        }
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(
        text="Loading and indexing company earnings calls – hang tight! This should take 1-2 minutes."
    ):
        client = LlamaIndexClient(
            openai_api_key=st.secrets["OPENAI_API_KEY"],
            qdrant_api_key=st.secrets["QDRANT_API_KEY"],
            qdrant_url=st.secrets["QDRANT_URL"],
        )
        client.build_engine()
        return client


client = load_data()

if "client" not in st.session_state.keys():
    st.session_state.client = client

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.client.query(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
