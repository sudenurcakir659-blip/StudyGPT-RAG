import os
import faiss
import numpy as np

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from utils import (
    clean_text,
    split_text,
    save_pickle,
    get_pdf_files,
    create_folder
)

# =====================================================
# KLASÖRLER
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PDF_FOLDER = os.path.join(BASE_DIR, "data", "pdf")

VECTOR_FOLDER = os.path.join(BASE_DIR, "vector_db")

INDEX_PATH = os.path.join(VECTOR_FOLDER, "vector.index")
CHUNKS_PATH = os.path.join(VECTOR_FOLDER, "chunks.pkl")
METADATA_PATH = os.path.join(VECTOR_FOLDER, "metadata.pkl")

MODEL_NAME = "all-MiniLM-L6-v2"

# =====================================================
# PDF OKUMA
# =====================================================

def extract_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    documents = []

    for page_no, page in enumerate(reader.pages):

        text = page.extract_text()

        text = clean_text(text)

        if text:

            documents.append({
                "text": text,
                "source": os.path.basename(pdf_path),
                "page": page_no + 1
            })

    return documents


# =====================================================
# PDF YÜKLE
# =====================================================

def load_documents():

    pdf_files = get_pdf_files(PDF_FOLDER)

    if len(pdf_files) == 0:

        print("PDF bulunamadı.")

        return []

    documents = []

    print("=" * 60)
    print("📚 PDF'ler okunuyor...")
    print("=" * 60)

    for pdf in pdf_files:

        print(f"\n📄 {os.path.basename(pdf)}")

        documents.extend(
            extract_pdf(pdf)
        )

    return documents


# =====================================================
# VECTOR DATABASE
# =====================================================

def create_vector_database():

    docs = load_documents()

    if len(docs) == 0:
        return

    chunks = []
    metadata = []

    print("\nChunk'lara ayrılıyor...")

    for doc in docs:

        parts = split_text(doc["text"])

        for part in parts:

            chunks.append(part)

            metadata.append({
                "source": doc["source"],
                "page": doc["page"]
            })

    print("\nEmbedding oluşturuluyor...")

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = embeddings.astype(np.float32)

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(embeddings)

    create_folder(VECTOR_FOLDER)

    faiss.write_index(
        index,
        INDEX_PATH
    )

    save_pickle(
        chunks,
        CHUNKS_PATH
    )

    save_pickle(
        metadata,
        METADATA_PATH
    )

    print("\n" + "=" * 60)
    print("🎉 BİLGİ BANKASI OLUŞTURULDU")
    print("=" * 60)

    print(f"PDF Sayısı   : {len(get_pdf_files(PDF_FOLDER))}")
    print(f"Chunk Sayısı : {len(chunks)}")
    print(f"Boyut        : {embeddings.shape[1]}")

    print("\nKaydedildi:")

    print(INDEX_PATH)
    print(CHUNKS_PATH)
    print(METADATA_PATH)


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    create_vector_database()