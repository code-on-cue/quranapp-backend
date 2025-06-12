import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("resources/df_quran_with_entities.csv")

# Pastikan kolom bersih dan tidak kosong
df['Tafsir_Bersih'] = df['Tafsir_Bersih'].fillna("")

# Fit TF-IDF ke seluruh tafsir
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Tafsir_Bersih'])

# Fungsi untuk melakukan pencarian semantik


def semantic_search(query, top_n=5):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarity.argsort()[-top_n:][::-1]
    return df.loc[top_indices, ['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Tafsir_Bersih']]


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
        return surah_detail[['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Tafsir_Bersih']]
    else:
        return pd.DataFrame(columns=['Surah', 'Nama_Surah_Indo', 'Ayat', 'Teks_Arab', 'Tafsir_Bersih'])
