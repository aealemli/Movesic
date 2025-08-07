from pydub import AudioSegment
import numpy as np
import os
import unicodedata
import re

songs_by_category = {
    "Klasik": [
        ("Chopin", "Songs/chopin-nocturne-in-e-flat-major-op-9-no-2.mp3"),
        ("Beethoven", "Songs/moonlight-sonata.mp3"),
        ("Vivaldi", "Songs/Vivaldi-The-Four-Seasons-Summer.mp3"),
        ("Mozart", "Songs/mozart-rondo-alla-turca.mp3")
    ],
    "Arabesk": [
        ("Paramparça", "Songs/Müslüm Gürses - Paramparça.mp3"),
        ("Hatasiz Kul olmaz", "Songs/Hatasız Kul Olmaz  - Orhan Gencebay.mp3"),
        ("Tutamiyorum Zamani", "Songs/Müslüm Gürses - Tutamıyorum Zamanı.mp3")
    ],
    "Pop": [
        ("Kirmizi", "Songs/Hande Yener - Kırmızı.mp3"),
        ("Kuzu Kuzu", "Songs/TARKAN - Kuzu Kuzu.mp3"),
        ("Karabiberim", "Songs/Serdar Ortaç - Karabiberim.mp3")
    ],
    "Metal": [
        ("Thunderstruck", "Songs/ACDC - Thunderstruck.mp3"),
        ("Fade to Black", "Songs/Fade To Black.mp3")        
    ],
    "Rock": [
        ("Mayin Tarlasi", "Songs/Mayın Tarlası.mp3"),
        ("Islak Islak", "Songs/Barış Akarsu - Islak Islak.mp3"),
        ("Her şeyi yak", "Songs/Duman - Her Şeyi Yak.mp3"),
        ("Can Kiriklari", "Songs/Şebnem Ferah - Can Kırıkları.mp3")
    ]
}

# Türkçe karakterleri siler ve dosya ismi güvenli hale getirir
def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '_', value)
    return value

output_folder = "Songs/npy_songs"
os.makedirs(output_folder, exist_ok=True)

for category, songs in songs_by_category.items():
    for name, path in songs:
        try:
            print(f"Processing: {name} | {path}")
            sound = AudioSegment.from_mp3(path)
            samples = np.array(sound.get_array_of_samples())

            # Stereo ise tek kanala indir
            if sound.channels == 2:
                samples = samples.reshape((-1, 2)).mean(axis=1)

            samples = samples / np.max(np.abs(samples))

            filename = f"{slugify(name)}.npy"
            full_path = os.path.join(output_folder, filename)
            np.save(full_path, samples)
            print(f"Saved: {full_path}")

        except Exception as e:
            print(f"Error processing {name}: {e}")
