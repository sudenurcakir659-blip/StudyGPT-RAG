import os
import pickle
import faiss
import streamlit as st

from google import genai
from sentence_transformers import SentenceTransformer


# =====================================================
# GEMINI
# =====================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise Exception(
        "GEMINI_API_KEY bulunamadı."
    )

client = genai.Client(
    api_key=api_key
)

MODELS = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]


# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VECTOR_FOLDER = os.path.join(BASE_DIR, "vector_db")

INDEX_PATH = os.path.join(VECTOR_FOLDER, "vector.index")
CHUNKS_PATH = os.path.join(VECTOR_FOLDER, "chunks.pkl")
METADATA_PATH = os.path.join(VECTOR_FOLDER, "metadata.pkl")


# =====================================================
# EMBEDDING MODEL
# =====================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =====================================================
# LOAD DATABASE
# =====================================================

def load_database():

    if not os.path.exists(INDEX_PATH):
        raise Exception("FAISS veritabanı bulunamadı.")

    index = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, chunks, metadata


# =====================================================
# SEARCH
# =====================================================

def search_documents(question, k=5):

    index, chunks, metadata = load_database()

    vector = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    distances, ids = index.search(vector, k)

    results = []

    for idx in ids[0]:

        if idx != -1 and idx < len(chunks):

            results.append(
                {
                    "text": chunks[idx],
                    "source": metadata[idx]["source"],
                    "page": metadata[idx]["page"]
                }
            )

    return results


# =====================================================
# ASK
# =====================================================

def ask(question):

    docs = search_documents(question)

    if len(docs) == 0:
        return "Bu soru için uygun ders içeriği bulunamadı."

    context = ""

    for doc in docs:

        context += f"""
Kaynak: {doc['source']}
Sayfa: {doc['page']}

{doc['text']}

-----------------------------------------
"""

    prompt = f"""
Sen StudyGPT isimli üniversite ders asistanısın.

Sadece aşağıdaki ders notlarını kullan.

Kurallar:

- Türkçe cevap ver.
- Bilgi uydurma.
- Bilgi yoksa "Bu bilgi ders notlarında bulunmuyor." de.
- Açıklayıcı anlat.

DERS NOTLARI

{context}

SORU

{question}
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text

    except Exception as e:

        return f"Gemini Hatası:\n\n{str(e)}"
