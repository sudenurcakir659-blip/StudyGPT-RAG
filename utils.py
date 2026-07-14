import os
import pickle
import re


# =====================================================
# Klasör oluşturma
# =====================================================

def create_folder(path):

    if not os.path.exists(path):
        os.makedirs(path)


# =====================================================
# Metin temizleme
# =====================================================

def clean_text(text):

    if text is None:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================================
# Metni parçalara ayırma (chunk)
# =====================================================

def split_text(
        text,
        chunk_size=500,
        overlap=50
):

    words = text.split()

    chunks = []

    start = 0


    while start < len(words):

        end = start + chunk_size


        chunk = " ".join(
            words[start:end]
        )


        chunks.append(
            chunk
        )


        start += chunk_size - overlap


    return chunks



# =====================================================
# Pickle kaydetme
# =====================================================

def save_pickle(
        data,
        file_path
):

    with open(
        file_path,
        "wb"
    ) as file:

        pickle.dump(
            data,
            file
        )



# =====================================================
# Pickle yükleme
# =====================================================

def load_pickle(
        file_path
):

    with open(
        file_path,
        "rb"
    ) as file:

        return pickle.load(
            file
        )



# =====================================================
# PDF dosyalarını bulma
# =====================================================

def get_pdf_files(
        folder
):

    pdf_files = []


    if not os.path.exists(folder):

        return pdf_files



    for file in os.listdir(folder):

        if file.lower().endswith(".pdf"):

            pdf_files.append(
                os.path.join(
                    folder,
                    file
                )
            )


    return pdf_files