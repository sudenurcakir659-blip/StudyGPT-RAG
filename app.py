import os
import subprocess
import streamlit as st

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

if os.path.exists("style.css"):

    with open(
        "style.css",
        "r",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"""
            <style>
            {f.read()}
            </style>
            """,
            unsafe_allow_html=True
        )



# =====================================================
# SESSION
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = []



# =====================================================
# KLASÖR
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


PDF_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "pdf"
)


os.makedirs(
    PDF_FOLDER,
    exist_ok=True
)



# =====================================================
# BAŞLIK
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


    st.header(
        "📚 StudyGPT Menü"
    )


    st.divider()


    mode = st.selectbox(
        "🎯 Çalışma Modu",
        [
            "📖 Ders Modu",
            "📝 Sınav Modu"
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



    if st.button(
        "💾 PDF'leri Kaydet",
        use_container_width=True
    ):


        if uploaded_files:


            for file in uploaded_files:


                file_path = os.path.join(
                    PDF_FOLDER,
                    file.name
                )


                with open(
                    file_path,
                    "wb"
                ) as f:


                    f.write(
                        file.getbuffer()
                    )


            st.success(
                "✅ PDF'ler kaydedildi."
            )


        else:


            st.warning(
                "PDF seçmelisin."
            )



    st.divider()



    if st.button(
        "🧠 Bilgi Bankasını Oluştur",
        use_container_width=True
    ):


        with st.spinner(
            "PDF'ler analiz ediliyor..."
        ):


            python_path = os.path.join(
                ".venv",
                "Scripts",
                "python.exe"
            )


            result = subprocess.run(
                [
                    python_path,
                    "ingest.py"
                ],
                capture_output=True,
                text=True
            )



            if result.returncode == 0:


                st.success(
                    "🎉 Bilgi bankası hazır!"
                )


            else:


                st.error(
                    result.stderr
                )



    st.divider()



    if st.button(
        "🗑️ Sohbeti Temizle",
        use_container_width=True
    ):


        st.session_state.messages = []

        st.rerun()



    st.info(
"""
🤖 **StudyGPT**

📚 PDF'lerini öğrenir

🧠 Bilgi bankası oluşturur

💬 Sorularını cevaplar
"""
)



# =====================================================
# CHAT GEÇMİŞİ
# =====================================================


st.markdown(
"## 💬 StudyGPT Sohbet"
)



for message in st.session_state.messages:


    if message["role"] == "user":


        st.markdown(
f"""
<div class="user-message">

👤 <b>Sen</b>

<br><br>

{message["content"]}

</div>
""",
unsafe_allow_html=True
)



    else:


        st.markdown(
f"""
<div class="ai-message">

🤖 <b>StudyGPT</b>

<br><br>

{message["content"]}

</div>
""",
unsafe_allow_html=True
)




# =====================================================
# SORU ALMA
# =====================================================


question = st.chat_input(
"StudyGPT'ye soru sor..."
)



if question:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )



    with st.spinner(
        "🤖 StudyGPT düşünüyor..."
    ):


        try:


            result = rag.ask_question(
                question
            )


            answer = result["answer"]



            if mode == "📝 Sınav Modu":


                answer = f"""
📌 **Sınav Odaklı Açıklama**

{answer}


⭐ **Sınav için önemli noktalar**

- Tanımları bil
- Temel mantığı öğren
- Formülleri tekrar et
- Örnek çöz
"""



            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":answer
                }
            )



        except Exception as e:


            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":f"❌ Hata oluştu: {e}"
                }
            )



    st.rerun()