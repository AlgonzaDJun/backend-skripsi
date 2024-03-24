import requests

API_URL = "https://api-inference.huggingface.co/models/cahya/bert-base-indonesian-NER"
headers = {"Authorization": "Bearer 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"}

sentences = [
    {
        "id_laporan": "65efc573bc23e31104b06e9e",
        "sentence": "lampu di food court danau unesa perlu diganti",
        "judul": "lampu food court",
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
        "id_laporan": "65efc573bc23e31104b06ea7",
        "sentence": "kondisi tempat duduk di food court sangat jelek",
        "judul": "kursi food court",
        "lokasi": "food court Danau Unesa Ketintang",
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
        "id_laporan": "65efc573bc23e31104b06e97",
        "sentence": "tempat duduk di food court danau unesa tidak nyaman",
        "judul": "Tempat duduk tidak nyaman di food court danau unesa",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
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
        "id_laporan": "65efc573bc23e31104b06ea3",
        "sentence": "kondisi kursi di food court sangat buruk",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
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
        "id_laporan": "65efc573bc23e31104b06e9f",
        "sentence": "kursi di food court danau unesa terlalu kotor",
        "judul": "kursi food court",
        "lokasi": "Food Court Danau Unesa Ketintang",
        "fakultas": "",
        "jurusan": "",
        "gambar": [],
    },
    {
        "id_laporan": "65efc573bc23e31104b06ea5",
        "sentence": "lampu di food court danau unesa tidak menyala",
        "judul": "lampu food court",
        "lokasi": "Food court danau unesa ketintang",
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
        "id_laporan": "65efc573bc23e31104b06eac",
        "sentence": "lampu di food court danau unesa berkedip kedip",
        "judul": "lampu di food court",
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
]
combined_sentences = ". ".join([sentence["sentence"] for sentence in sentences])


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query(
    {
        "inputs": combined_sentences,
    }
)

print(output)

# for item in output:
#     print(f"Entity Group: {item['entity_group']}")
#     print(f"Score: {item['score']}")
#     print(f"Word: {item['word']}")
#     print(f"Start: {item['start']}")
#     print(f"End: {item['end']}")
#     print()
