from pydub import AudioSegment
import numpy as np
import os
import unicodedata
import re

songs_by_category = {
    "Klasik": [
        ("Chopin", "FULLPATH/Songs/chopin-nocturne-in-e-flat-major-op-9-no-2.mp3"),
        ("Beethoven", "FULLPATH/Songs/moonlight-sonata.mp3"),
        ("Vivaldi", "FULLPATH/Songs/Vivaldi-The-Four-Seasons-Summer.mp3"),
        ("Mozart", "FULLPATH/Songs/mozart-rondo-alla-turca.mp3")
    ],
    "Arabesk": [
        ("Paramparça", "FULLPATH/Songs/Müslüm Gürses - Paramparça.mp3"),
        ("Hatasiz Kul olmaz", "FULLPATH/Songs/Hatasız Kul Olmaz  - Orhan Gencebay.mp3"),
        ("Tutamiyorum Zamani", "FULLPATH/Songs/Müslüm Gürses - Tutamıyorum Zamanı.mp3")
    ],
    "Pop": [
        ("Kirmizi", "FULLPATH/Songs/Hande Yener - Kırmızı.mp3"),
        ("Kuzu Kuzu", "FULLPATH/Songs/TARKAN - Kuzu Kuzu.mp3"),
        ("Karabiberim", "FULLPATH/Songs/Serdar Ortaç - Karabiberim.mp3")
    ],
    "Metal": [
        ("Thunderstruck", "FULLPATH/Songs/ACDC - Thunderstruck.mp3"),
        ("Fade to Black", "FULLPATH/Songs/Fade To Black.mp3")        
    ],
    "Rock": [
        ("Mayin Tarlasi", "FULLPATH/Songs/Mayın Tarlası.mp3"),
        ("Islak Islak", "FULLPATH/Songs/Barış Akarsu - Islak Islak.mp3"),
        ("Her şeyi yak", "FULLPATH/Songs/Duman - Her Şeyi Yak.mp3"),
        ("Can Kiriklari", "FULLPATH/Songs/Şebnem Ferah - Can Kırıkları.mp3")
    ]
}

# Türkçe karakterleri siler ve dosya ismi güvenli hale getirir
def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '_', value)
    return value

output_folder = "FULLPATH/Songs/npy_songs"
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
