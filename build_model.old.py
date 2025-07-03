import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("resources/df_quran_with_entities.csv")

# Pastikan kolom bersih dan tidak kosong
df['Isi_Bersih'] = df['Isi_Bersih'].fillna("")

# Fit TF-IDF ke seluruh tafsir
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Isi_Bersih'])

# Fungsi untuk melakukan pencarian semantik


def get_recommendation_from_history(history_list, top_n=10):
    if not history_list:
        return pd.DataFrame(columns=['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan'])

    combined_query = " ".join(history_list)
    return semantic_search(combined_query, top_n)


def search_by_query(query):
    """Melakukan pencarian berdasarkan query."""
    if not query or len(query) < 3:
        return pd.DataFrame(columns=['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan', 'Tafsir_Jalalain', 'Tafsir_Mukhtasar'])

    # match terjemahan yang mengandung query
    return df[df['Terjemahan'].str.contains(query, case=False, na=False)]


def semantic_search(query, top_n=10):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarity.argsort()[-top_n:][::-1]

    result = df.loc[top_indices, ['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan', 'Tafsir_Jalalain', 'Tafsir_Mukhtasar']].copy()
    result['similarity'] = similarity[top_indices]
    
    return result


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
        return surah_detail[['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan', 'Tafsir_Jalalain', 'Tafsir_Mukhtasar']]
    else:
        return pd.DataFrame(columns=['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Terjemahan', 'Tafsir_Jalalain', 'Tafsir_Mukhtasar'])
