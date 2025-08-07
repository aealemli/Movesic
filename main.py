import cv2
import mediapipe as mp
import numpy as np
import math
import pygame
import time
import os
import unicodedata
from menu_utils import draw_arc_menu, draw_cat_menu, confirm_fingertips, get_menu_index


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
current_songs = []

categories= ["Klasik","Arabesk","Pop","Metal","Rock"]

output_folder = "Songs/npy_songs"


def normalize(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return text.lower()
waveforms = {}
for filename in os.listdir(output_folder):
    if filename.endswith(".npy"):
        key = filename[:-4]  
        waveforms[key] = np.load(os.path.join(output_folder, filename))

is_paused=False
COOLDOWN_TIME = 10
cooldown = 0
fist_threshold = 50
menu_open = False
menu_index = -1
menu_center = None

category_menu_index = -1
song_menu_index = -1


song_index = 0
song_name = None
samples = None
sample_rate = None
start_time_wave = None

selected_category_idx = -1
current_phase = "category"

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)



npy_files_mapping = {
    "Chopin": "chopin.npy",
    "Beethoven": "beethoven.npy",
    "Vivaldi": "vivaldi.npy",
    "Mozart": "mozart.npy",
    "Paramparça": "paramparca.npy",
    "Hatasiz Kul olmaz": "hatasiz_kul_olmaz.npy",
    "Tutamiyorum Zamani": "tutamiyorum_zamani.npy",
    "Kirmizi": "kirmizi.npy",
    "Kuzu Kuzu": "kuzu_kuzu.npy",
    "Karabiberim": "karabiberim.npy",
    "Thunderstruck": "thunderstruck.npy",
    "Fade to Black": "fade_to_black.npy",
    "Mayin Tarlasi": "mayin_tarlasi.npy",
    "Islak Islak": "islak_islak.npy",
    "Her şeyi yak": "her_seyi_yak.npy",
    "Can Kiriklari": "can_kiriklari.npy"
}

waveforms = {}
for category, songs in songs_by_category.items():
    for song_name, path in songs:
        key = normalize(song_name)
        npy_name = f"{key.replace(' ', '_').replace('ı','i').replace('ç','c')}.npy"
        full_path = os.path.join(output_folder, npy_name)
        if os.path.exists(full_path):
            waveforms[key] = np.load(full_path)
        else:
            print(f"UYARI: {npy_name} bulunamadı")


def calculate_distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

def is_fist(lm):
    return all(calculate_distance(lm[0], lm[tip]) < fist_threshold for tip in [8, 12, 16, 20])

def is_confirm(lm):
    return calculate_distance(lm[4], lm[8]) < 40

def get_pixel_coords(landmark, frame):
    h, w = frame.shape[:2]
    return int(landmark.x * w), int(landmark.y * h)

def midpoint(p1, p2):
    return ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

def draw_wave_between_points(img, pt1, pt2, vol, samples, sample_rate, start_time, color=(255, 255, 255)):
    if pt1 is None or pt2 is None:
        return

    pt1 = np.array(pt1, dtype=np.float32)
    pt2 = np.array(pt2, dtype=np.float32)

    direction = pt2 - pt1
    length = np.linalg.norm(direction)
    if length == 0:
        return

    direction /= length 

    normal = np.array([-direction[1], direction[0]])

    elapsed_time = time.time() - start_time
    N = int(np.clip(length, 30, 200))
    start_sample = int(elapsed_time * sample_rate)
    segment = samples[start_sample:start_sample + N]

    if len(segment) < N:
        segment = np.pad(segment, (0, N - len(segment)))

    amplitude = int(vol * 100)

    for i in range(N - 1):
        alpha1 = i / (N - 1)
        alpha2 = (i + 1) / (N - 1)

        base1 = pt1 + direction * (length * alpha1)
        base2 = pt1 + direction * (length * alpha2)

        y1 = base1 + normal * segment[i] * amplitude
        y2 = base2 + normal * segment[i+1] * amplitude

        cv2.line(img,
                 tuple(np.int32(y1)),
                 tuple(np.int32(y2)),
                 color, 2)

def draw_wave_between_hands(frame, handL, handR, vol, samples, sample_rate, start_time, color=(0, 255, 0)):
    if handL is None or handR is None:
        return

    p4L = get_pixel_coords(handL.landmark[4], frame)
    p8L = get_pixel_coords(handL.landmark[8], frame)
    p4R = get_pixel_coords(handR.landmark[4], frame)
    p8R = get_pixel_coords(handR.landmark[8], frame)

    start_point = midpoint(p4L, p8L)
    end_point = midpoint(p4R, p8R)

    width = end_point[0] - start_point[0]
    height = end_point[1] - start_point[1]

    elapsed_time = time.time() - start_time
    window_size = 1024
    start_sample = int(elapsed_time * sample_rate)
    end_sample = start_sample + window_size

    if end_sample > len(samples):
        return  
    
    segment = samples[start_sample:end_sample]
    if len(segment) < window_size:
        segment = np.pad(segment, (0, window_size - len(segment)))

    amplitude = int(vol * 100)  
    
    points = []
    for i in range(window_size - 1):
        x = int(start_point[0] + (width * i) / window_size)
        y_base = int(start_point[1] + (height * i) / window_size)
        y_wave = int(segment[i] * amplitude)
        points.append((x, y_base - y_wave))

    for i in range(1, len(points)):
        cv2.line(frame, points[i-1], points[i], color, 2)

while True:

    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    h, w, _ = img.shape

    vol = pygame.mixer.music.get_volume()
    control_mode = "Bekleniyor"
    hands_data = []
    confirm_L = False
    confirm_R = False
    fist_detected = False
    hand_landmarks_L = None
    hand_landmarks_R = None

    if results.multi_hand_landmarks:

        for handLms, handInfo in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handInfo.classification[0].label
            lm = [(int(pt.x * w), int(pt.y * h)) for pt in handLms.landmark]
            hands_data.append((label, lm))

            color = (0,255,0) if label == 'Right' else (255,0,0)
            for tip in [4, 8]:
                cv2.circle(img, lm[tip], 8, color, 2)

            if label == 'Left':
                hand_landmarks_L = handLms
                if is_confirm(lm):
                    confirm_L = True
                    confirm_fingertips(hand_landmarks_L,img)
            if label == 'Right':
                hand_landmarks_R = handLms
                if is_confirm(lm):
                    confirm_fingertips(hand_landmarks_R, img)
                    if cooldown == 0:
                        if not menu_open:
                            menu_open = True
                            current_phase = "category"
                            selected_category_idx = -1
                        else:
                            if current_phase == "category":
                                menu_open = False
                                menu_center = None
                                selected_category_idx = -1
                                current_phase = "category"
                            elif current_phase =="song":
                                menu_open = False
                                menu_center = None
                                selected_category_idx = -1
                        cooldown = COOLDOWN_TIME


    SMOOTHING_FACTOR = 0.2
    
    if menu_open:
        right_hand = [lm for label, lm in hands_data if label == 'Right']
        if right_hand:
            lm = right_hand[0]
            target_x = lm[0][0]
            target_y = lm[0][1] - 100

            if menu_center is None:
                menu_center = (target_x, target_y)
            else:
                new_x = int(menu_center[0] + SMOOTHING_FACTOR * (target_x - menu_center[0]))
                new_y = int(menu_center[1] + SMOOTHING_FACTOR * (target_y - menu_center[1]))
                menu_center = (new_x, new_y)

            idx_tip = right_hand[0][8]
            if current_songs:
                cat_index = get_menu_index(menu_center,idx_tip,len(categories))
                menu_index = get_menu_index(menu_center, idx_tip, len(current_songs))

            if current_phase == "category":
                category_menu_index = get_menu_index(menu_center, idx_tip, len(categories))
                draw_cat_menu(img, menu_center, 200, categories, category_menu_index)
                if confirm_L and cooldown == 0:
                    selected_category_idx = category_menu_index
                    selected_category = categories[selected_category_idx]
                    current_songs = songs_by_category[selected_category] 
                    current_phase = "song"
                    cooldown = COOLDOWN_TIME
            elif current_phase == "song":
                song_menu_index = get_menu_index(menu_center, idx_tip, len(current_songs))
                draw_arc_menu(img, menu_center, 200, current_songs, song_menu_index)
                if confirm_L and cooldown == 0:
                    song_index = song_menu_index
                    song_name, song_path = current_songs[song_index] 
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play(-1)

                    samples = waveforms [normalize(song_name)].astype(np.float32)
                    samples = samples / np.max(np.abs(samples))
                    sample_rate = 44100
                    start_time_wave = time.time()

                    menu_open = False
                    menu_center = None
                    current_phase = "category"
                    cooldown = COOLDOWN_TIME
                    

    elif confirm_L and cooldown == 0 and not menu_open:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            is_paused = True
            start_time_wave = None
            cooldown = COOLDOWN_TIME
        elif is_paused:
            pygame.mixer.music.unpause()
            pos_ms = pygame.mixer.music.get_pos()  
            start_time_wave = time.time() - (pos_ms / 1000.0)
            samples = waveforms[normalize(song_name)].astype(np.float32)
            samples = samples / np.max(np.abs(samples))
            sample_rate = 44100
            is_paused = False        
        
        cooldown = COOLDOWN_TIME


    if samples is not None and sample_rate is not None and start_time_wave is not None:
        if hand_landmarks_L is not None and hand_landmarks_R is not None:
            draw_wave_between_hands(img, hand_landmarks_L, hand_landmarks_R, vol, samples, sample_rate, start_time_wave)
        elif hand_landmarks_L is not None or hand_landmarks_R is not None:
            hand = hand_landmarks_L if hand_landmarks_L is not None else hand_landmarks_R
            point1 = tuple(np.multiply(
                [hand.landmark[4].x, hand.landmark[4].y],
                [img.shape[1], img.shape[0]]
            ).astype(int))

            point2 = tuple(np.multiply(
                [hand.landmark[8].x, hand.landmark[8].y],
                [img.shape[1], img.shape[0]]
            ).astype(int))

            distance = np.linalg.norm(np.array(point1) - np.array(point2))
            draw_wave_between_points(img, point1, point2, vol, samples, sample_rate, start_time_wave)


    left = [lm for label, lm in hands_data if label == 'Left']
    right = [lm for label, lm in hands_data if label == 'Right']
    if left and right:
        d = calculate_distance(left[0][4], right[0][4])
        vol = np.interp(d, [30, 700], [0.0, 1.0])
        pygame.mixer.music.set_volume(vol)
        control_mode = "iki el: Ses"

    else:
        for _, lm in hands_data:
            d = calculate_distance(lm[4], lm[8])
            vol = np.interp(d, [35, 200], [0.0, 1.0])
            pygame.mixer.music.set_volume(vol)
            control_mode = "Tek el: Ses"


    cv2.putText(img, f"Ses: {int(vol*100)}% ({control_mode})", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    if current_songs and 0 <= song_index < len(current_songs):
     cv2.putText(img, f"Caliyor: {current_songs[song_index][0]}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("El ile Muzik Kontrol", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cooldown > 0:
        cooldown -= 1

print("waveforms keys:", list(waveforms.keys()))
print("normalize edilmiş song_name:", normalize(song_name))

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()