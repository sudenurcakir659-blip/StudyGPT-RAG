import os
import faiss
import pickle

from google import genai
from sentence_transformers import SentenceTransformer


# =====================================================
# GEMINI CLIENT
# =====================================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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
# ASK
# =====================================================

def ask(question):

    docs = search_documents(question)

    if len(docs) == 0:
        return "Bu soru için uygun içerik bulunamadı."

    context = ""

    for doc in docs:

        context += f"""
Kaynak: {doc['source']}
Sayfa: {doc['page']}

{doc['text']}

---------------------------------------
"""

    prompt = f"""
Sen StudyGPT isimli üniversite ders asistanısın.

Sadece verilen ders notlarını kullan.

Bilgi yoksa bilmiyorum de.

Ders Notları:

{context}

Soru:

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
