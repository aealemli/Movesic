# 🎵 Movesic – El Hareketleriyle Müzik Kontrol Sistemi

Bu proje, **MediaPipe** ve **Pygame** kullanılarak geliştirilen, el hareketleriyle müzik seçme, başlatma/durdurma ve ses seviyesi kontrolü yapılabilen yenilikçi bir müzik çalar sistemidir. Kullanıcı, fiziksel temas olmadan sadece ellerini kullanarak müzikle etkileşime geçebilir ve aynı zamanda gerçek zamanlı ses dalgası görselleştirmeleriyle estetik bir deneyim yaşar.

## 📌 Özellikler

- 🤚 **Sağ el ile menü açma**: Menü açıldığında yarım daire şeklinde şarkı seçenekleri belirir.
- 👈 **Sol el ile seçim yapma**: Baş parmak ve işaret parmağı birleştirilerek seçim yapılır.
- 🔁 **Dinamik kontrol**: Menü ikinci kez açıldığında kapanır. Aynı şarkıya tekrar tıklanırsa öneri paneli kapanır.
- 🔊 **Tek elle ses kontrolü**: Parmaklar arası mesafeye göre ses seviyesi ayarlanır.
- 🔊 **Çift elle ses kontrolü**: Avuçlar arası mesafeye göre ses seviyesi ayarlanır.
- 🎶 **Gerçek zamanlı waveform (ses dalgası) görselleştirmesi**.
- 💾 **Performans optimizasyonu**: MP3 dosyaları önceden `.npy` formatına dönüştürülerek hızlı erişim sağlanır.
- 👁️‍🗨️ **Görsel geri bildirim**: Tıklama animasyonları ve akıcı dalga çizimi.

## 📂 Dosya Yapısı

###Movesic/
 - main.py # Ana uygulama (el hareketiyle kontrol)
 - audio_visualizer.py # Pygame ile ses dalgası çizimi 
 - menu.utils.py # Menü çizimi ve seçim işlemleri
 - preprocess.py # MP3 dosyalarını .npy formatına çevirir
 ├── Songs/ # MP3 müzik dosyaları
 │ └── Songs/ # MP3’lerden dönüştürülen .npy dosyaları
 ├── dist/ # .exe oluşturulmuşsa burada yer alır (yüklenecek değil)
 ├── build/ # PyInstaller derleme dosyaları (yüklenecek değil)
 ├── pycache/ # Python cache klasörü (yüklenecek değil)
 ├── main.spec # PyInstaller yapı dosyası
 └── README.md # Proje açıklaması

## 🛠️ Kullanılan Teknolojiler

- **Python 3.12**
- **MediaPipe** – El hareketi algılama
- **Pygame** – Arayüz ve çizim
- **Pydub** – MP3 işleme
- **Simpleaudio** – Ses çalma
- **NumPy** – Ses verisi analizi
- **OpenCV** – Kameradan görüntü alma

# 🚀 Kurulum ve Kullanım

### 1. Gerekli bağımlılıkları yükleyin:
`pip install mediapipe pygame pydub simpleaudio numpy opencv-python`
### 2. ffmpeg'i sisteminize yükleyin:
 ffmpeg, MP3 dosyalarının işlenebilmesi için zorunludur.
 https://ffmpeg.org/download.html adresinden indirip sistem PATH'ine eklemeyi unutmayın.

### 3. MP3 dosyalarınızı 'songs/' klasörüne yerleştirin:
 Örnek klasör yapısı:
 ├── Songs/
 │   ├── music1.mp3
 │   ├── music2.mp3

### 4. Dosya adlarında Türkçe karakter, boşluk veya özel semboller olmamalı:
 Şarkılarınızı yükledikten sonra hem `main.py`, hem de `audio_visualizer.py` dosyaları
 içerisine şarkı isim ve konumlarını doğru yazdığınızdan ve türkçe karakter kullanmadığınızdan
 emin olun.

# 2. MP3 dosyalarını .npy formatına dönüştürün:
`python audiovisualizer.py`
 Bu işlemden sonra klasör yapınız şu şekilde görünecektir:
 ├── songs/
 │   ├── music1.mp3
 │   ├── music2.mp3

# 3. Uygulamayı başlatın:
`python main.py`

# 🧠 Nasıl Çalışıyor?
## Kamera açılır ve MediaPipe ile el pozisyonları izlenir.
- Sağ el menüyü açar; yarım çember şeklinde şarkılar gösterilir.
- Sol el ile seçim yapılır. Baş ve işaret parmaklarının teması tıklama olarak algılanır.

## Şarkıya ait .npy verisi belleğe yüklenir.
- Pygame ile gerçek zamanlı ses dalgası çizilir.

### Eğer tek el varsa
- Eldeki parmak açıklığına göre ses seviyesi kontrol edilir.

### Her iki el de kameraya görünüyorsa
- Ellerin arasındaki mesafeye göre ses seviyesi belirlenir.

# 📝 Lisans
## Bu proje GNU Affero General Public License v3.0 (AGPL-3.0) lisansı ile lisanslanmıştır.
## Projeyi ticari olarak kullanmayı düşünüyorsanız lisans koşullarını dikkatlice okuyunuz.
## AGPLv3 lisansı, kaynak kodun türetilmiş projelerde de açık kalmasını şart koşar.

# 👤 Geliştirici
# Abdullah Ege Alemli – Türkiye
