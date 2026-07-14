import streamlit as st
import os
import rag


# =====================================================
# SAYFA AYARI
# =====================================================

st.set_page_config(
    page_title="StudyGPT",
    page_icon="📚",
    layout="wide"
)


# =====================================================
# CSS
# =====================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f8f9fa;
    }

    .title {
        font-size: 45px;
        font-weight: 800;
        color: #4F46E5;
        text-align:center;
    }

    .subtitle {
        text-align:center;
        color:#555;
        font-size:18px;
    }

    .chat-box {
        padding:15px;
        border-radius:15px;
        background:white;
        margin-bottom:10px;
        box-shadow:0 2px 8px #ddd;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="title">📚 StudyGPT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Yapay Zeka Destekli Ders Asistanı</div>',
    unsafe_allow_html=True
)


st.divider()


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =====================================================
# CHAT GEÇMİŞİ
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])



# =====================================================
# USER INPUT
# =====================================================

prompt = st.chat_input(
    "Sorunu yaz..."
)


if prompt:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )


    with st.chat_message("user"):
        st.write(prompt)



    # =================================================
    # RAG SORGU
    # =================================================

    with st.chat_message("assistant"):

        with st.spinner("Düşünüyorum..."):

            try:

                response = rag.ask(
                    prompt
                )


                st.write(response)


                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":response
                    }
                )


            except Exception as e:


                error_message = (
                    "Bir hata oluştu:\n\n"
                    + str(e)
                )


                st.error(
                    error_message
                )


                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":error_message
                    }
                )



# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "StudyGPT © 2026 | FAISS + RAG + Gemini"
)