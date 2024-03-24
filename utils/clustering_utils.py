from sklearn.cluster import KMeans
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from collections import Counter
import re, string, unicodedata
import pandas as pd
from googletrans import Translator
import json
import spacy

# from .summarize import summarize_text_offline, summarize_text_online

# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory #import Indonesian Stemmer
# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory #import stopword sastrawi

nltk.download("punkt")
nltk.download("stopwords")

# def stemmingIndo(str):
#     factory = StemmerFactory()
#     stemmer = factory.create_stemmer()
#     return stemmer.stem(str)


def cleaning(str):
    # remove non-ascii
    str = (
        unicodedata.normalize("NFKD", str)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
    )
    # remove URLs
    str = re.sub(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        "",
        str,
    )
    # remove punctuations
    str = re.sub(r"[^\w]|_", " ", str)
    # remove digit from string
    str = re.sub("\S*\d\S*", "", str).strip()
    # remove digit or numbers
    str = re.sub(r"\b\d+\b", " ", str)
    # to lowercase
    str = str.lower()
    # Remove additional white spaces
    str = re.sub("[\s]+", " ", str)

    return str


# Contoh data kalimat
# sentences = [
#     "Di food court danau unesa ketintang, kursi ada yang rusak.",
#     "Tempat sampah belum ada di danau unesa ketintang.",
#     "Kursi di food court perlu diperbaiki.",
#     "Saya menemukan banyak sampah di sekitar danau unesa.",
#     "Listrik di ruang food court sering mati tiba-tiba.",
#     "Tempat duduk di food court danau unesa tidak nyaman.",
#     "Kursi di food court danau unesa sering patah.",
#     "Saya menemukan beberapa kerusakan di kursi food court.",
#     "Sampah menumpuk di dekat danau unesa ketintang.",
#     "Listrik di food court danau unesa sering padam.",
#     "Kursi di food court butuh perbaikan segera.",
#     "Saya merasa tidak aman di sekitar danau unesa pada malam hari.",
#     "Lampu di food court danau unesa perlu diganti.",
#     "Kursi di food court danau unesa terlalu kotor.",
#     "Saya menemukan tempat sampah yang penuh di food court.",
#     "Listrik di danau unesa ketintang terputus-putus.",
#     "Kursi di food court danau unesa tidak kokoh lagi.",
#     "Kondisi kursi di food court sangat buruk.",
#     "Saya tidak bisa menemukan tempat sampah di sekitar danau unesa.",
#     "Lampu di food court danau unesa tidak menyala.",
#     "Kursi di food court danau unesa terasa tidak aman.",
#     "Kondisi tempat duduk di food court sangat jelek.",
#     "Listrik di food court danau unesa sering bergoyang.",
#     "Saya khawatir dengan keamanan di danau unesa ketintang.",
#     "Sampah berserakan di food court danau unesa ketintang.",
#     "Kursi di food court danau unesa sangat tidak nyaman.",
#     "Lampu di food court danau unesa berkedip-kedip.",
#     "Kursi di food court danau unesa kurang terawat.",
#     "Saya merasa gelap di sekitar danau unesa ketintang.",
#     "Tempat sampah di food court danau unesa penuh.",
#     "Listrik di food court danau unesa sangat lemah.",
#     "Kursi di food court danau unesa sudah sangat usang.",
# ]


def perform_clustering(sentences):
    stop_words = set(stopwords.words("indonesian"))

    tokenize_words = [word_tokenize(cleaning(word)) for word in sentences]
    filtered_words = [
        [word for word in tokenize_word if word.lower() not in stop_words]
        for tokenize_word in tokenize_words
    ]
    # filtered_words = tokenize_words
    clean_words = [" ".join(sentence) for sentence in filtered_words]
    # print(clean_words)

    # Preprocessing dan tokenisasi
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(clean_words)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray())

    # print(clean_words)
    # print(tfidf_df)

    # Melakukan clustering dengan K-Means
    num_clusters = 5  # Ganti dengan jumlah cluster yang diinginkan
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)

    # Menyusun kalimat ke dalam cluster
    clusters = {}
    for i, label in enumerate(kmeans.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(clean_words[i])

    # Fungsi untuk mengidentifikasi kata-kata yang sering muncul dalam cluster
    def identify_most_common_words(cluster):
        # Menggabungkan semua kalimat dalam cluster menjadi satu teks
        combined_text = " ".join(cluster)
        # Menghitung kata-kata yang sering muncul dalam cluster
        word_counts = Counter(combined_text.split())
        # Mengambil kata-kata yang paling sering muncul (misalnya, 3 kata teratas)
        most_common_words = word_counts.most_common(4)  # Ubah angka 3 sesuai kebutuhan
        return [word[0] for word in most_common_words]

    # print hasil clustering
    # for cluster_id, sentences_in_cluster in clusters.items():
    #     most_common_words = identify_most_common_words(sentences_in_cluster)
    #     cluster_name = ", ".join(most_common_words)
    #     print(f"Cluster {cluster_id + 1} ({cluster_name}):")
    #     for sentence in sentences_in_cluster:
    #         print(f"- {sentence}")

    result = []
    for cluster_id, sentences_in_cluster in clusters.items():
        most_common_words = identify_most_common_words(sentences_in_cluster)
        result.append(
            {
                "cluster_id": cluster_id + 1,
                "sentences": sentences_in_cluster,
                "most_common_words": most_common_words,
            }
        )

    return result


def perform_clustering_dev(laporans, jumlah_cluster):
    stop_words = set(stopwords.words("indonesian"))

    sentences = [laporan["deskripsi"] for laporan in laporans]

    tokenize_words = [word_tokenize(cleaning(word)) for word in sentences]
    filtered_words = [
        [word for word in tokenize_word if word.lower() not in stop_words]
        for tokenize_word in tokenize_words
    ]
    # filtered_words = tokenize_words
    clean_words = [" ".join(sentence) for sentence in filtered_words]
    not_clean_words = [" ".join(sentence) for sentence in tokenize_words]

    # print(clean_words)

    # Preprocessing dan tokenisasi
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(clean_words)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray())

    # print(clean_words)
    # print(tfidf_df)

    # Melakukan clustering dengan K-Means
    num_clusters = jumlah_cluster  # Ganti dengan jumlah cluster yang diinginkan
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)

    # Menyusun kalimat ke dalam cluster
    clusters = {}
    for i, label in enumerate(kmeans.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(
            {
                "id_laporan": str(laporans[i]["_id"]),
                "sentence": clean_words[i],
                "sentence_not_clean": not_clean_words[i],
                "judul": laporans[i]["judul"],
                "lokasi": laporans[i]["lokasi"],
                "fakultas": laporans[i]["fakultas"],
                "jurusan": laporans[i]["jurusan"],
                "gambar": laporans[i]["gambar"],
            }
        )

    # Fungsi untuk mengidentifikasi kata-kata yang sering muncul dalam cluster
    def identify_most_common_words(cluster):
        # Menggabungkan semua kalimat dalam cluster menjadi satu teks
        combined_text = " ".join(cluster)
        # Menghitung kata-kata yang sering muncul dalam cluster
        word_counts = Counter(combined_text.split())
        # Mengambil kata-kata yang paling sering muncul (misalnya, 3 kata teratas)
        most_common_words = word_counts.most_common(4)  # Ubah angka 3 sesuai kebutuhan
        return [word[0] for word in most_common_words]

    # Menghitung jumlah anggota setiap cluster
    cluster_sizes = {
        cluster_id: len(sentences_in_cluster)
        for cluster_id, sentences_in_cluster in clusters.items()
    }

    # Mengurutkan cluster berdasarkan jumlah anggota
    sorted_clusters = sorted(cluster_sizes.items(), key=lambda x: x[1], reverse=True)

    # result = []
    # for cluster_id, sentences_in_cluster in clusters.items():
    #     most_common_words = identify_most_common_words(
    #         [sentence["sentence"] for sentence in sentences_in_cluster]
    #     )
    #     result.append(
    #         {
    #             "cluster_id": str(cluster_id + 1),
    #             "sentences": sentences_in_cluster,
    #             "most_common_words": most_common_words,
    #         }
    #     )
    result = []
    for cluster_id, _ in sorted_clusters:
        sentences_in_cluster = clusters[cluster_id]
        # Menggabungkan semua kalimat dalam cluster menjadi satu string
        # sentence_string = ". ".join(
        #     [sentence["sentence"] for sentence in sentences_in_cluster]
        # )
        not_clean_sentence_string = ". ".join(
            [sentence["sentence_not_clean"] for sentence in sentences_in_cluster]
        )
        # summary_text = summarize_text_online(not_clean_sentence_string)
        most_common_words = identify_most_common_words(
            [sentence["sentence"] for sentence in sentences_in_cluster]
        )
        result.append(
            {
                "cluster_id": str(cluster_id + 1),
                "sentences": sentences_in_cluster,
                "most_common_words": most_common_words,
                # "summarize_text": summary_text,
                "not_clean_sentence_string": not_clean_sentence_string,
                "jumlah_anggota": len(sentences_in_cluster),
            }
        )

    return result


def perform_ner(laporans, jml_cluster):
    stop_words = set(stopwords.words("indonesian"))

    sentences = [laporan["deskripsi"] for laporan in laporans]

    tokenize_words = [word_tokenize(cleaning(word)) for word in sentences]
    filtered_words = [
        [word for word in tokenize_word if word.lower() not in stop_words]
        for tokenize_word in tokenize_words
    ]
    # filtered_words = tokenize_words
    clean_words = [" ".join(sentence) for sentence in filtered_words]
    not_clean_words = [" ".join(sentence) for sentence in tokenize_words]

    # print(clean_words)

    # Preprocessing dan tokenisasi
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(clean_words)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray())

    # print(clean_words)
    # print(tfidf_df)

    # Melakukan clustering dengan K-Means
    num_clusters = jml_cluster  # Ganti dengan jumlah cluster yang diinginkan
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)

    # Menyusun kalimat ke dalam cluster
    clusters = {}
    for i, label in enumerate(kmeans.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(
            {
                "id_laporan": str(laporans[i]["_id"]),
                "sentence": not_clean_words[i],
                "judul": laporans[i]["judul"],
                "lokasi": laporans[i]["lokasi"],
                "fakultas": laporans[i]["fakultas"],
                "jurusan": laporans[i]["jurusan"],
                "gambar": laporans[i]["gambar"],
            }
        )

    # Fungsi untuk mengidentifikasi kata-kata yang sering muncul dalam cluster
    def identify_most_common_words(cluster):
        # Menggabungkan semua kalimat dalam cluster menjadi satu teks
        combined_text = " ".join(cluster)
        # Menghitung kata-kata yang sering muncul dalam cluster
        word_counts = Counter(combined_text.split())
        # Mengambil kata-kata yang paling sering muncul (misalnya, 3 kata teratas)
        most_common_words = word_counts.most_common(4)  # Ubah angka 3 sesuai kebutuhan
        return [word[0] for word in most_common_words]

    # Menghitung jumlah anggota setiap cluster
    cluster_sizes = {
        cluster_id: len(sentences_in_cluster)
        for cluster_id, sentences_in_cluster in clusters.items()
    }

    # Mengurutkan cluster berdasarkan jumlah anggota
    sorted_clusters = sorted(cluster_sizes.items(), key=lambda x: x[1], reverse=True)

    # result = []
    # for cluster_id, sentences_in_cluster in clusters.items():
    #     most_common_words = identify_most_common_words(
    #         [sentence["sentence"] for sentence in sentences_in_cluster]
    #     )
    #     result.append(
    #         {
    #             "cluster_id": str(cluster_id + 1),
    #             "sentences": sentences_in_cluster,
    #             "most_common_words": most_common_words,
    #         }
    #     )
    result = []
    for cluster_id, _ in sorted_clusters:
        sentences_in_cluster = clusters[cluster_id]
        # Menggabungkan semua kalimat dalam cluster menjadi satu string
        sentence_string = ". ".join(
            [sentence["sentence"] for sentence in sentences_in_cluster]
        )
        hasil_ner = ekstraksi_ner(sentence_string)
        hasil_ner_trans = ekstraksi_ner_trans(sentence_string)
        most_common_words = identify_most_common_words(
            [sentence["sentence"] for sentence in sentences_in_cluster]
        )
        jml_anggota = len(sentences_in_cluster)
        result.append(
            {
                "cluster_id": str(cluster_id + 1),
                "sentences": sentences_in_cluster,
                "most_common_words": most_common_words,
                "NER": hasil_ner,
                "NER_TRANS": hasil_ner_trans,
                "jumlah_anggota": jml_anggota,
            }
        )

    return result


import requests

API_URL = "https://api-inference.huggingface.co/models/cahya/bert-base-indonesian-NER"
headers = {"Authorization": "Bearer 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"}


def ekstraksi_ner(sentences):

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query(
        {
            "inputs": sentences,
        }
    )

    # # Urutkan entitas berdasarkan skornya
    # sorted_entities = sorted(output, key=lambda x: x["score"], reverse=True)

    # # Ambil lima entitas dengan skor tertinggi
    # top_5_entities = sorted_entities[:5]

    unique_words = set()  # Set untuk menyimpan kata-kata unik
    result = []  # List untuk menyimpan hasil tanpa duplikat

    for item in output:
        word = item["word"]
        if word not in unique_words:
            unique_words.add(word)
            result.append(item)

    return result


def ekstraksi_ner_trans(sentences):
    translator = Translator()
    translation = translator.translate(sentences, dest="en", src="id")
    # print(f"translation: {translation.text}")
    after_translation = translation.text

    # Load the spacy engine:
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(after_translation)

    def translate_to_indonesian(text):
        translation = translator.translate(text, dest="id", src="en")
        return translation.text

    # Menerjemahkan setiap entitas secara terpisah dan membangun list of dictionaries
    unique_translations = set()
    translations = []
    for ent in doc.ents:
        # if ent.start < len(doc) and ent.end <= len(doc):
        #     translated_text = translate_to_indonesian(ent.text)
        #     translations.append({"text": str(translated_text), "label": ent.label_})
        if ent.start < len(doc) and ent.end <= len(doc):
            translated_text = translate_to_indonesian(ent.text)
            if translated_text not in unique_translations:
                unique_translations.add(translated_text)
                translations.append({"text": str(translated_text), "label": ent.label_})

    return {"entities": translations}


from sklearn.metrics import silhouette_score
import plotly.graph_objects as go
import plotly.io as pio


def find_optimal_num_clusters_silhouette(laporans, max_clusters=10):
    stop_words = set(stopwords.words("indonesian"))

    sentences = [laporan["deskripsi"] for laporan in laporans]

    tokenize_words = [word_tokenize(cleaning(word)) for word in sentences]
    filtered_words = [
        [word for word in tokenize_word if word.lower() not in stop_words]
        for tokenize_word in tokenize_words
    ]
    # filtered_words = tokenize_words
    clean_words = [" ".join(sentence) for sentence in filtered_words]
    not_clean_words = [" ".join(sentence) for sentence in tokenize_words]

    # print(clean_words)

    # Preprocessing dan tokenisasi
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(clean_words)
    data = tfidf_matrix
    silhouette_scores = []
    for num_clusters in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=num_clusters)
        cluster_labels = kmeans.fit_predict(data)
        silhouette_avg = silhouette_score(data, cluster_labels)
        silhouette_scores.append(silhouette_avg)

    # Generate data for react-chartjs2
    chart_data = {
        "labels": list(range(2, max_clusters + 1)),
        "datasets": [
            {
                "label": "Silhouette Score",
                "data": silhouette_scores,
                "fill": False,
                "borderColor": "rgb(75, 192, 192)",
                "lineTension": 0.1,
            }
        ],
    }

    return chart_data


def find_optimal_num_clusters_silhouette_chart(laporans, max_clusters=10):
    stop_words = set(stopwords.words("indonesian"))

    sentences = [laporan["deskripsi"] for laporan in laporans]

    tokenize_words = [word_tokenize(cleaning(word)) for word in sentences]
    filtered_words = [
        [word for word in tokenize_word if word.lower() not in stop_words]
        for tokenize_word in tokenize_words
    ]
    # filtered_words = tokenize_words
    clean_words = [" ".join(sentence) for sentence in filtered_words]
    not_clean_words = [" ".join(sentence) for sentence in tokenize_words]

    # print(clean_words)

    # Preprocessing dan tokenisasi
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(clean_words)
    data = tfidf_matrix
    silhouette_scores = []
    for num_clusters in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=num_clusters)
        cluster_labels = kmeans.fit_predict(data)
        silhouette_avg = silhouette_score(data, cluster_labels)
        silhouette_scores.append(silhouette_avg)

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(2, max_clusters + 1)),
            y=silhouette_scores,
            mode="lines+markers",
        )
    )

    fig.update_layout(
        xaxis_title="Number of clusters",
        yaxis_title="Silhouette Score",
        title="Silhouette Method",
    )

    # Convert Plotly figure to HTML
    plot_html = pio.to_html(fig, full_html=False)

    return plot_html