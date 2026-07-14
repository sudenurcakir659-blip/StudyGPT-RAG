import streamlit as st
import os
import rag
import ingest


# =====================================================
# PAGE
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

.stApp{
    background:#080f24;
    color:white;
}


section[data-testid="stSidebar"]{
    background:#0b1228;
}


h1,h2,h3,p,label{
    color:white !important;
}


.title{
    text-align:center;
    font-size:70px;
    font-weight:700;
    color:#7c8cff;
}


.subtitle{
    text-align:center;
    font-size:22px;
    color:#cbd5ff;
}


.card{
    background:#111936;
    padding:25px;
    border-radius:20px;
    margin:20px;
}


button{
    border-radius:15px !important;
}


</style>
""",
unsafe_allow_html=True
)



# =====================================================
# HEADER
# =====================================================

st.markdown(
"""
<div class="title">
📂 StudyGPT
</div>

<div class="subtitle">
Yapay Zeka Destekli Kişisel Ders Çalışma Asistanın 🚀
</div>

<br>

<div class="subtitle">
PDF yükle • Öğren • Soru sor
</div>

""",
unsafe_allow_html=True
)



# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:


    st.markdown(
    """
    # 📚 StudyGPT Menü
    """
    )


    st.divider()


    st.subheader(
        "🎯 Çalışma Modu"
    )


    mode = st.selectbox(
        "",
        [
            "📖 Ders Modu",
            "📝 Soru Çözme Modu"
        ]
    )


    st.divider()


    st.subheader(
        "📄 PDF Yönetimi"
    )


    uploaded_files = st.file_uploader(
        "Ders PDF'lerini yükle",
        type=["pdf"],
        accept_multiple_files=True
    )


    st.caption(
        "200MB per file • PDF"
    )


    if st.button(
        "📚 PDF'leri Kaydet",
        use_container_width=True
    ):


        if uploaded_files:


            os.makedirs(
                "documents",
                exist_ok=True
            )


            for file in uploaded_files:

                path = os.path.join(
                    "documents",
                    file.name
                )


                with open(
                    path,
                    "wb"
                ) as f:

                    f.write(
                        file.getbuffer()
                    )


            st.success(
                "PDF'ler kaydedildi!"
            )


            st.info(
                "Bilgi bankası için ingest çalıştırılmalı."
            )


        else:

            st.warning(
                "Önce PDF yükle."
            )


    st.divider()


    st.button(
        "🧠 Bilgi Bankasını Oluştur",
        use_container_width=True
    )



# =====================================================
# CHAT
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages=[]



for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )



question = st.chat_input(
    "Dersin hakkında soru sor..."
)



if question:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )


    with st.chat_message("user"):

        st.write(question)



    with st.chat_message("assistant"):


        with st.spinner(
            "StudyGPT düşünüyor..."
        ):


            try:


                answer = rag.ask(
                    question
                )


                st.write(
                    answer
                )


                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":answer
                    }
                )


            except Exception as e:


                st.error(
                    str(e)
                )



# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "StudyGPT | FAISS + RAG + Gemini"
)
