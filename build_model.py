import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch


# Load dataframe
df = pd.read_pickle("resources/tafsir_dataset.pkl")

try:
    print("🔄 Loading corpus embeddings...")
    corpus_embeddings = torch.load("resources/corpus_embeddings.pt")
    print("✅ Embeddings loaded:", corpus_embeddings.shape)
except Exception as e:
    print("❌ Gagal load embeddings:", e)
    corpus_embeddings = None  # biar gak crash seluruh server

# Load model SBERT Multilingual
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

def get_recommendation_from_history(history_list, top_n=10):
    if not history_list:
        return pd.DataFrame(columns=['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan'])

    combined_query = " ".join(history_list)
    return semantic_search(combined_query, top_n)


def search_by_query(query):
    """Melakukan pencarian berdasarkan query."""
    if not query or len(query) < 3:
        return pd.DataFrame(columns=['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan', 'Tafsir_Jalalain'])

    # match terjemahan yang mengandung query
    return df[df['Terjemahan'].str.contains(query, case=False, na=False)]

def semantic_search(query, top_n=10):
    query_embedding = model.encode(query, convert_to_tensor=True).cpu()  # Force ke CPU
    corpus_cpu = corpus_embeddings.cpu()  # pastikan ini juga di CPU

    cosine_scores = util.cos_sim(query_embedding, corpus_cpu)[0]
    top_results = torch.topk(cosine_scores, k=top_n)

    hasil = df.iloc[top_results[1].numpy()].copy()
    hasil['similarity'] = top_results[0].numpy()
    return hasil

# def semantic_search(query, top_n=10):
#     query_vec = vectorizer.transform([query])
#     similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
#     top_indices = similarity.argsort()[-top_n:][::-1]

#     result = df.loc[top_indices, ['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan', 'Tafsir_Jalalain']].copy()
#     result['similarity'] = similarity[top_indices]
    
#     return result


# Fungsi untuk mengambil daftar surah dan nama surah
def get_surah_list():
    """Mengambil daftar surah dari DataFrame."""
    surah_list = df[['Surah', 'Nama_Surah_Indo']
                    ].drop_duplicates().sort_values(by='Surah')
    return surah_list.reset_index(drop=True)


# Fungsi untuk mengambil detail surah berdasarkan nomor surah
def get_surah_detail(surah_number):
    """Mengambil detail surah berdasarkan nomor surah."""
    surah_detail = df[df['Surah'] == surah_number]
    if not surah_detail.empty:
        return surah_detail[['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan', 'Tafsir_Jalalain']]
    else:
        return pd.DataFrame(columns=['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan', 'Tafsir_Jalalain'])
