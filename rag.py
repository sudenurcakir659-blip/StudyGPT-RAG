import os
import faiss
import requests

from sentence_transformers import SentenceTransformer
from utils import load_pickle

# =====================================================
# KLASÖRLER
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VECTOR_FOLDER = os.path.join(BASE_DIR, "vector_db")

INDEX_PATH = os.path.join(VECTOR_FOLDER, "vector.index")
CHUNKS_PATH = os.path.join(VECTOR_FOLDER, "chunks.pkl")
METADATA_PATH = os.path.join(VECTOR_FOLDER, "metadata.pkl")

# =====================================================
# OLLAMA
# =====================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:4b"

# =====================================================
# EMBEDDING MODEL
# =====================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =====================================================
# DATABASE
# =====================================================

def load_vector_database():

    if not os.path.exists(INDEX_PATH):
        raise Exception(
            "Bilgi bankası bulunamadı.\n\n"
            "Önce 'Bilgi Bankasını Oluştur' butonuna bas."
        )

    index = faiss.read_index(INDEX_PATH)

    chunks = load_pickle(CHUNKS_PATH)

    metadata = load_pickle(METADATA_PATH)

    return index, chunks, metadata


# =====================================================
# ARAMA
# =====================================================

def search_context(question, top_k=5):

    index, chunks, metadata = load_vector_database()

    embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(
        embedding,
        top_k
    )

    context = []

    for idx in indices[0]:

        if idx == -1:
            continue

        context.append({
            "text": chunks[idx],
            "source": metadata[idx]["source"],
            "page": metadata[idx]["page"]
        })

    return context


# =====================================================
# PROMPT
# =====================================================

def create_prompt(question, context):

    sources = ""

    for item in context:

        sources += f"""

Kaynak: {item["source"]}
Sayfa: {item["page"]}

{item["text"]}

------------------------------------------------
"""

    prompt = f"""
Sen StudyGPT isimli akademik yardımcı asistansın.

Sadece aşağıdaki kaynakları kullan.

Kurallar:

- Kaynak dışına çıkma.
- Bilgi uydurma.
- Eğer cevap kaynaklarda yoksa
  "Kaynaklarda bu bilgi bulunamadı."
  yaz.

KAYNAKLAR:

{sources}

SORU:

{question}

CEVAP:
"""

    return prompt


# =====================================================
# OLLAMA
# =====================================================

def ask_ollama(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]


# =====================================================
# ANA FONKSİYON
# =====================================================

def ask_question(question):

    context = search_context(question)

    prompt = create_prompt(
        question,
        context
    )

    answer = ask_ollama(prompt)

    return {
        "answer": answer,
        "sources": context
    }


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    while True:

        q = input("\nSoru (q=çıkış): ")

        if q.lower() == "q":
            break

        result = ask_question(q)

        print("\n")
        print(result["answer"])

        print("\nKaynaklar\n")

        for s in result["sources"]:

            print(
                f"{s['source']} - Sayfa {s['page']}"
            )