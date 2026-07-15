import streamlit as st
import os
import rag
import ingest


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="StudyGPT",
    page_icon="📚",
    layout="wide"
)


# =====================================================
# LOAD CSS
# =====================================================

def load_css():

    if os.path.exists("style.css"):

        with open(
            "style.css",
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


load_css()



# =====================================================
# HEADER
# =====================================================

st.markdown(
"""
<div class="main-title">
📚 StudyGPT
</div>

<div class="subtitle">
Yapay Zeka Destekli Kişisel Ders Çalışma Asistanın 🚀
<br>
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
        "PDF desteklenir"
    )


    if st.button(
        "📚 PDF'leri Kaydet",
        use_container_width=True
    ):


        if uploaded_files:


            os.makedirs(
                "data/pdf",
                exist_ok=True
            )


            for file in uploaded_files:


                path = os.path.join(
                    "data/pdf",
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
                "PDF'ler kaydedildi ✅"
            )


            st.info(
                "Bilgi bankası oluşturmayı unutma."
            )


        else:

            st.warning(
                "Önce PDF yükle."
            )



    st.divider()



    if st.button(
    "🧠 Bilgi Bankasını Oluştur",
    use_container_width=True
):

    with st.spinner("Bilgi bankası hazırlanıyor..."):

        try:

            ingest.create_vector_database()

            st.success("🎉 Bilgi bankası başarıyla oluşturuldu.")

        except Exception as e:

            st.error(f"Hata: {e}") 


            except Exception as e:

                st.error(
                    str(e)
                )




# =====================================================
# CHAT MEMORY
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = []




# =====================================================
# SHOW OLD MESSAGES
# =====================================================

for msg in st.session_state.messages:


    if msg["role"] == "user":


        st.markdown(
        f"""
        <div class="user-message">

        👤 {msg["content"]}

        </div>
        """,
        unsafe_allow_html=True
        )


    else:


        st.markdown(
        f"""
        <div class="ai-message">

        🤖 {msg["content"]}

        </div>
        """,
        unsafe_allow_html=True
        )





# =====================================================
# CHAT INPUT
# =====================================================


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


    st.markdown(
    f"""
    <div class="user-message">

    👤 {question}

    </div>
    """,
    unsafe_allow_html=True
    )



    with st.spinner(
        "StudyGPT düşünüyor... 🧠"
    ):


        try:


            answer = rag.ask(
                question
            )


            st.markdown(
            f"""
            <div class="ai-message">

            🤖 {answer}

            </div>
            """,
            unsafe_allow_html=True
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
