import os
import faiss
import pickle

import google.generativeai as genai
from sentence_transformers import SentenceTransformer 


# =====================================================
# KLASÖRLER
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

VECTOR_FOLDER = os.path.join(
    BASE_DIR,
    "vector_db"
)


INDEX_PATH = os.path.join(
    VECTOR_FOLDER,
    "vector.index"
)

CHUNKS_PATH = os.path.join(
    VECTOR_FOLDER,
    "chunks.pkl"
)

METADATA_PATH = os.path.join(
    VECTOR_FOLDER,
    "metadata.pkl"
)



# =====================================================
# MODELLER
# =====================================================

MODEL_NAME = "all-MiniLM-L6-v2"


embedding_model = SentenceTransformer(
    MODEL_NAME
)



# =====================================================
# GEMINI AYARI
# =====================================================

api_key = os.getenv(
    "GEMINI_API_KEY"
)


if api_key:

    genai.configure(
        api_key=api_key
    )


model = genai.GenerativeModel(
    "gemini-1.5-flash"
)



# =====================================================
# DATABASE YÜKLE
# =====================================================

def load_database():

    if not os.path.exists(INDEX_PATH):

        raise Exception(
            "FAISS veritabanı bulunamadı."
        )


    index = faiss.read_index(
        INDEX_PATH
    )


    with open(
        CHUNKS_PATH,
        "rb"
    ) as f:

        chunks = pickle.load(f)


    with open(
        METADATA_PATH,
        "rb"
    ) as f:

        metadata = pickle.load(f)


    return index, chunks, metadata



# =====================================================
# BENZER DOKÜMAN ARAMA
# =====================================================

def search_documents(
        question,
        k=5
):


    index, chunks, metadata = load_database()


    vector = embedding_model.encode(
        [question],
        convert_to_numpy=True
    )


    vector = vector.astype(
        "float32"
    )


    distances, ids = index.search(
        vector,
        k
    )


    results = []


    for idx in ids[0]:

        if idx < len(chunks):

            results.append(
                {
                    "text": chunks[idx],
                    "source": metadata[idx]["source"],
                    "page": metadata[idx]["page"]
                }
            )


    return results



# =====================================================
# RAG CEVAP
# =====================================================

def ask(question):


    documents = search_documents(
        question
    )


    if not documents:

        return (
            "Bu soru için uygun ders içeriği bulunamadı."
        )



    context = ""


    for doc in documents:

        context += f"""

Kaynak:
{doc['source']}

Sayfa:
{doc['page']}

İçerik:
{doc['text']}

----------------------

"""



    prompt = f"""

Sen StudyGPT isimli üniversite ders asistanısın.

Öğrencinin sorusunu sadece verilen ders
içeriğine dayanarak cevapla.

Kurallar:
- Türkçe cevap ver.
- Açıklayıcı anlat.
- Gereksiz bilgi ekleme.
- Bilgi yoksa belirt.


DERS İÇERİĞİ:

{context}


SORU:

{question}

"""


    response = model.generate_content(
        prompt
    )


    return response.text