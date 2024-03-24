import spacy

# load existing model
output_dir = "dataset/nlp_id_checkpoint_old"
print("Loading from", output_dir)
nlp_updated = spacy.load(output_dir)

sentences = [
    {
        "id_laporan": "65efc573bc23e31104b06ea0",
        "sentence": "saya menemukan tempat sampah yang penuh di food court",
        "judul": "tempat sampah penuh",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e99",
        "sentence": "saya menemukan beberapa kerusakan di kursi food court",
        "judul": "kerusakan kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06eae",
        "sentence": "tempat sampah di food court danau unesa penuh",
        "judul": "tempat sampah di food court",
        "lokasi": "Food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
]

sentences = [
    {
        "id_laporan": "65efc573bc23e31104b06e94",
        "sentence": "kursi food court diperbaiki",
        "judul": "Kursi food court perlu diperbaiki",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e96",
        "sentence": "listrik ruang food court mati",
        "judul": "Listrik sering mati di food court danau unesa",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [
            "https://id.benweilight.com/Content/uploads/2021779622/20211220161452d730c8ccfae94fd09ba8f382d2663d4d.jpg",
            "https://images.tokopedia.net/img/cache/500-square/VqbcmM/2022/4/9/9648fa9e-a2a0-4574-9200-79c13c46a661.jpg.webp?ect=4g",
        ],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e98",
        "sentence": "kursi food court danau unesa patah",
        "judul": "kursi food court sering patah",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e9b",
        "sentence": "listrik food court danau unesa padam",
        "judul": "listrik padam",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e9c",
        "sentence": "kursi food court butuh perbaikan",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06e9f",
        "sentence": "kursi food court danau unesa kotor",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea2",
        "sentence": "kursi food court danau unesa kokoh",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea3",
        "sentence": "kondisi kursi food court buruk",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea6",
        "sentence": "kursi food court danau unesa aman",
        "judul": "kursi food court",
        "lokasi": "food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea8",
        "sentence": "listrik food court danau unesa bergoyang",
        "judul": "listrik food court",
        "lokasi": "food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ead",
        "sentence": "kursi food court danau unesa terawat",
        "judul": "kursi di food court",
        "lokasi": "Food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06eaf",
        "sentence": "listrik food court danau unesa lemah",
        "judul": "listrik di food court",
        "lokasi": "Food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06eb0",
        "sentence": "kursi food court danau unesa usang",
        "judul": "kursi di food court",
        "lokasi": "Food court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
]

combined_sentences = ". ".join([sentence["sentence"] for sentence in sentences])
# combined_sentences = "pulau sialan itu ada dimana"

print(combined_sentences)

# doc = nlp_updated(combined_sentences)
# print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
