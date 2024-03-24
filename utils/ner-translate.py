from googletrans import Translator
from deep_translator import GoogleTranslator
import json
import spacy

sentences = [
    {
        "id_laporan": "65efc573bc23e31104b06e92",
        "sentence": "di food court danau unesa ketintang kursi ada yang rusak",
        "judul": "Food court kursi rusak",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e94",
        "sentence": "kursi di food court perlu diperbaiki",
        "judul": "Kursi food court perlu diperbaiki",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e97",
        "sentence": "tempat duduk di food court danau unesa tidak nyaman",
        "judul": "Tempat duduk tidak nyaman di food court danau unesa",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e98",
        "sentence": "kursi di food court danau unesa sering patah",
        "judul": "kursi food court sering patah",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e9c",
        "sentence": "kursi di food court butuh perbaikan segera",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e9d",
        "sentence": "saya merasa tidak aman di sekitar danau unesa pada malam hari",
        "judul": "tidak aman di danau",
        "lokasi": "Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e9f",
        "sentence": "kursi di food court danau unesa terlalu kotor",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea2",
        "sentence": "kursi di food court danau unesa tidak kokoh lagi",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea3",
        "sentence": "kondisi kursi di food court sangat buruk",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea6",
        "sentence": "kursi di food court danau unesa terasa tidak aman",
        "judul": "kursi food court",
        "lokasi": "food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea7",
        "sentence": "kondisi tempat duduk di food court sangat jelek",
        "judul": "kursi food court",
        "lokasi": "food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea9",
        "sentence": "saya khawatir dengan keamanan di danau unesa ketintang",
        "judul": "keamanan diri",
        "lokasi": "Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06eab",
        "sentence": "kursi di food court danau unesa sangat tidak nyaman",
        "judul": "Kursi di food court",
        "lokasi": "Food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ead",
        "sentence": "kursi di food court danau unesa kurang terawat",
        "judul": "kursi di food court",
        "lokasi": "Food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06eb0",
        "sentence": "kursi di food court danau unesa sudah sangat usang",
        "judul": "kursi di food court",
        "lokasi": "Food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06eb1",
        "sentence": "saya merasa gelap di sekitar danau unesa ketintang",
        "judul": "gelap di danau unesa",
        "lokasi": "Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
]


combined_sentences = ". ".join([sentence["sentence"] for sentence in sentences])

translator = Translator()
translate = translator.translate("the unesa ketintang lake", dest="id", src="en")
print(f"translate ke indonesia: {translate.text}")

translated = GoogleTranslator(source="en", target="id").translate(
    "the Unesa Ketintang Lake"
)
print(translated)

# translation = translator.translate(combined_sentences, dest="en")
# print(f"translation: {translation.text}")
# after_translation = translation.text


# # Load the spacy engine:
# nlp = spacy.load("en_core_web_sm")

# doc = nlp(after_translation)


# def translate_to_indonesian(text):
#     translation = translator.translate(text, dest="id")
#     return translation.text


# # Menerjemahkan setiap entitas secara terpisah dan membangun list of dictionaries
# translations = []
# for ent in doc.ents:
#     if ent.start < len(doc) and ent.end <= len(doc):
#         translated_text = translate_to_indonesian(ent.text)
#         translations.append({"text": (translated_text), "label": ent.label_})

# # Membuat objek JSON
# translations_json = json.dumps({"translations": translations})

# print(translations_json)
