#menu_utils.py
import cv2
import math
import time
import numpy as np


def draw_cat_menu(img,center,radius,cats,selected_idx):
    total = len(cats)
    for i,name in enumerate(cats):
        angle = math.pi * (i + 1) / (total + 1)
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] - radius * math.sin(angle))
        color = (0, 255, 0) if i == selected_idx else (180, 180, 180)
        cv2.circle(img, (x, y), 30, color, -1)
        cv2.putText(img, name, (x - 20, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20,20,20), 2)

def draw_arc_menu(img, center, radius, songs, selected_idx):
    total = len(songs)
    for i, (name, _) in enumerate(songs):
        angle = math.pi * (i + 1) / (total + 1)
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] - radius * math.sin(angle))
        color = (0, 255, 0) if i == selected_idx else (180, 180, 180)
        cv2.circle(img, (x, y), 30, color, -1)
        cv2.putText(img, name, (x - 20, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20,20,20), 2)

def get_menu_index(center, finger_tip, num_options):
    dx = finger_tip[0] - center[0]
    dy = center[1] - finger_tip[1]
    angle = math.atan2(dy, dx)
    if angle < 0:
        angle += math.pi
    per_section = math.pi / num_options
    return min(int(angle / per_section), num_options - 1)

def confirm_fingertips(hand,img):
    confirm_flash_time = time.time()

    point1 = tuple(np.multiply(
        [hand.landmark[4].x, hand.landmark[4].y],
        [img.shape[1], img.shape[0]]
    ).astype(int))

    point2 = tuple(np.multiply(
        [hand.landmark[8].x, hand.landmark[8].y],
        [img.shape[1], img.shape[0]]
    ).astype(int))
    if time.time() - confirm_flash_time < 1:
        cv2.circle(img, point1, 8, (0, 255, 0), -1)
        cv2.circle(img, point2, 8, (0, 255, 0), -1)
    else:
        cv2.circle(img, point1, 8, (0, 255, 0), 2)
        cv2.circle(img, point2, 8, (0, 255, 0), 2)
