# StudyGPT-RAG

<div align="center">

## Yapay Zeka Destekli Ders Asistanı

StudyGPT-RAG, yüklenen ders PDF'lerinden bilgi çıkararak öğrencilerin sorularını kendi dokümanları üzerinden cevaplayan **Retrieval Augmented Generation (RAG)** tabanlı bir yapay zeka çalışma asistanıdır.

</div>

---

##  Proje Hakkında

StudyGPT-RAG, öğrencilerin ders materyallerini daha verimli kullanabilmesi amacıyla geliştirilmiş bir yapay zeka destekli soru-cevap sistemidir.

Kullanıcılar PDF formatındaki ders notlarını sisteme yükleyerek:

-  Ders notları üzerinden soru sorabilir
- İlgili içerikleri hızlıca bulabilir
-  Yapay zeka destekli açıklamalar alabilir
-  Kendi kişisel bilgi bankasını oluşturabilir

Sistem klasik chatbotlardan farklı olarak cevaplarını doğrudan yüklenen kaynaklardan üretir.

---

#  Özellikler

✅ PDF dokümanlarından otomatik bilgi çıkarma  
✅ RAG (Retrieval Augmented Generation) mimarisi  
✅ FAISS vektör veritabanı kullanımı  
✅ Semantic Search ile ilgili içerik bulma  
✅ Yapay zeka destekli cevap üretimi  
✅ Streamlit web arayüzü  
✅ Kişisel ders bilgi bankası oluşturma  
✅ Hızlı ve kullanıcı dostu arayüz  

---

#  Sistem Mimarisi 
PDF Dosyaları
|
↓
Metin Çıkarma (PyPDF)
|
↓
Metin Parçalama
|
↓
Embedding Model
(Sentence Transformers)
|
↓
FAISS Vector Database
|
↓
Kullanıcı Sorusu
|
↓
Benzer İçerik Arama
|
↓
LLM (Gemini)
|
↓
AI Destekli Cevap  

---

#  Kullanılan Teknolojiler

## Backend

- Python
- FAISS
- Sentence Transformers
- PyPDF
- Google Gemini API

## Frontend

- Streamlit

## Yapay Zeka

- Retrieval Augmented Generation (RAG)
- Embedding Models
- Large Language Models (LLM)

---

# Proje Yapısı
StudyGPT-RAG
│
├── app.py # Streamlit kullanıcı arayüzü
├── rag.py # RAG sistemi ve AI cevap üretimi
├── ingest.py # PDF işleme ve vektör oluşturma
├── utils.py # Yardımcı fonksiyonlar
├── style.css # Arayüz tasarımı
│
├── data/
│ └── pdf/ # Ders PDF dosyaları
│
├── vector_db/
│ ├── vector.index # FAISS index
│ ├── chunks.pkl # Metin parçaları
│ └── metadata.pkl # Kaynak bilgileri
│
├── requirements.txt
└── README.md
# ⚙️ Kurulum

## 1. Repository'i klonlayın

```bash
git clone https://github.com/sudenurcakir659-blip/StudyGPT-RAG.git
2. Sanal ortam oluşturun
python -m venv .venv

Aktifleştirme:

Windows:

.venv\Scripts\activate
3. Kütüphaneleri yükleyin
pip install -r requirements.txt
API Ayarları

Google Gemini API anahtarınızı ekleyin.

.env veya Streamlit Secrets:

GEMINI_API_KEY="YOUR_API_KEY"
Bilgi Bankası Oluşturma

PDF dosyalarınızı:

data/pdf/

klasörüne ekleyin.

Daha sonra:

python ingest.py

veya uygulama üzerinden:

Bilgi Bankasını Oluştur

butonuna basın.


Örnek:

"Paging ve segmentation arasındaki fark nedir?"

StudyGPT ilgili ders notlarını bularak açıklamalı cevap üretir.

- RAG Nedir?

RAG (Retrieval Augmented Generation), yapay zekanın cevap üretmeden önce ilgili bilgileri bir veri kaynağından aramasını sağlayan mimaridir.

Bu proje:

Kullanıcı sorusunu analiz eder.
FAISS üzerinde benzer içerikleri arar.
Bulunan içerikleri LLM'e gönderir.
Kaynak destekli cevap üretir.

-Projenin Amacı

Bu projenin amacı öğrencilerin:

Ders çalışma süresini azaltmak
Notlara hızlı erişim sağlamak
Kişisel yapay zeka çalışma asistanına sahip olmak

için RAG teknolojisini kullanmaktır.

-Geliştirici

Sudenur Çakır

Computer Engineering Student

GitHub:
https://github.com/sudenurcakir659-blip

