#FINAL CODE AS OF NOW
import cv2
import numpy as np
import os
import os
import yaml
from collections import defaultdict
from ultralytics import YOLO
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

CONSTELLATION_DATA = {
# =====================================================
# ZODIAC CONSTELLATIONS
# =====================================================
'Aqr': {
'name': 'Aquarius',
'star_points': [
(500, 350), (400, 200), (350, 150), (550, 180), (250, 400),
(200, 600), (450, 800), (600, 900), (750, 850), (900, 700)
],
'connections': [
(1, 2), (1, 3), (1, 0), (0, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)
]
},
'Ari': {
'name': 'Aries',
'star_points': [(500, 500), (400, 450), (300, 480)],
'connections': [(0, 1), (1, 2)]
},
'Cnc': {
'name': 'Cancer',
'star_points': [(500, 400), (600, 500), (500, 600), (400, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0)]
},
'Cap': {
'name': 'Capricornus',
'star_points': [(100, 500), (300, 600), (500, 550), (700, 450), (600, 300), (400, 350), (250, 400)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)]
},
'Gem': {
'name': 'Gemini',
'star_points': [(200, 200), (250, 500), (300, 800), (600, 200), (550, 500), (500, 800)],
'connections': [(0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (1, 4)]
},
'Leo': {
'name': 'Leo',
'star_points': [(200, 200), (300, 300), (400, 400), (350, 500), (250, 600), (150, 500), (700, 400), (900, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (2, 6), (6, 7)]
},
'Lib': {
'name': 'Libra',
'star_points': [(300, 300), (700, 300), (200, 600), (800, 600)],
'connections': [(0, 1), (0, 2), (1, 3), (2, 3)]
},
'Psc': {
'name': 'Pisces',
'star_points': [(200, 800), (300, 700), (400, 600), (500, 500), (600, 400), (700, 300), (800, 200), (750, 500), (700, 600), (650, 700)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7), (7, 8), (8, 9), (9, 2)]
},
'Sag': {
'name': 'Sagittarius',
'star_points': [(600, 400), (700, 600), (600, 800), (400, 800), (300, 600), (400, 400), (200, 200)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (5, 4), (5, 6)]
},
'Sco': {
'name': 'Scorpius',
'star_points': [(200, 200), (400, 200), (600, 200), (500, 400), (500, 600), (500, 800), (700, 900), (300, 900)],
'connections': [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (5, 6), (5, 7)]
},
'Tau': {
'name': 'Taurus',
'star_points': [(800, 200), (600, 400), (500, 500), (400, 400), (200, 200)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)]
},
'Vir': {
'name': 'Virgo',
'star_points': [(200, 800), (300, 600), (400, 400), (600, 400), (800, 600), (700, 800), (500, 500)],
'connections': [(0, 1), (1, 2), (2, 6), (3, 6), (3, 4), (4, 5)]
},
# =====================================================
# NORTHERN HEMISPHERE CONSTELLATIONS
# =====================================================
'And': {
'name': 'Andromeda',
'star_points': [(419, 102), (408, 206), (403, 394), (510, 422), (692, 532), (308, 412), (118, 513)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6)]
},
'Aql': {
'name': 'Aquila',
'star_points': [(500, 500), (500, 400), (500, 600), (200, 300), (850, 350), (150, 800)],
'connections': [(1, 0), (0, 2), (3, 0), (4, 0), (2, 5)]
},
'Aur': {
'name': 'Auriga',
'star_points': [(500, 100), (300, 300), (400, 500), (600, 500), (700, 300)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
},
'Boo': {
'name': 'Bootes',
'star_points': [(500, 100), (400, 300), (300, 500), (500, 700), (700, 500), (600, 300)],
'connections': [(0, 1), (0, 5), (1, 2), (2, 3), (3, 4), (4, 5)]
},
'Cam': {
'name': 'Camelopardalis',
'star_points': [(100, 800), (300, 700), (500, 600), (400, 400), (200, 300), (450, 200), (700, 100)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (5, 6)]
},
'Cas': {
'name': 'Cassiopeia',
'star_points': [(100, 500), (300, 350), (500, 500), (700, 350), (900, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4)]
},
'Cep': {
'name': 'Cepheus',
'star_points': [(500, 700), (300, 500), (350, 300), (650, 300), (700, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
},
'Com': {
'name': 'Coma Berenices',
'star_points': [(300, 600), (500, 500), (600, 300)],
'connections': [(0, 1), (1, 2)]
},
'CrB': {
'name': 'Corona Borealis',
'star_points': [(200, 500), (400, 350), (600, 350), (800, 500), (700, 650), (500, 700), (300, 650)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)]
},
'CVn': {
'name': 'Canes Venatici',
'star_points': [(400, 600), (600, 400)],
'connections': [(0, 1)]
},
'Cyg': {
'name': 'Cygnus',
'star_points': [(500, 350), (500, 500), (500, 900), (200, 500), (800, 500)],
'connections': [(0, 1), (1, 2), (3, 1), (1, 4)]
},
'Del': {
'name': 'Delphinus',
'star_points': [(400, 400), (600, 400), (550, 300), (450, 300), (500, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4)]
},
'Dra': {
'name': 'Draco',
'star_points': [(800, 800), (700, 600), (600, 400), (500, 200), (300, 250), (200, 450), (350, 600), (550, 700), (400, 100), (200, 150)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (3, 8), (4, 9), (8, 9)]
},
'Equ': {
'name': 'Equuleus',
'star_points': [(400, 300), (600, 350), (550, 500), (350, 450)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0)]
},
'Her': {
'name': 'Hercules',
'star_points': [(300, 200), (700, 200), (200, 400), (800, 400), (200, 600), (800, 600), (300, 800), (700, 800)],
'connections': [(0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (2, 3), (4, 5), (2, 6), (3, 7)]
},
'Lac': {
'name': 'Lacerta',
'star_points': [(200, 200), (400, 300), (500, 500), (400, 700), (200, 800)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4)]
},
'LMi': {
'name': 'Leo Minor',
'star_points': [(300, 300), (500, 500), (700, 400)],
'connections': [(0, 1), (1, 2)]
},
'Lyn': {
'name': 'Lynx',
'star_points': [(200, 800), (400, 600), (600, 400), (800, 200)],
'connections': [(0, 1), (1, 2), (2, 3)]
},
'Lyr': {
'name': 'Lyra',
'star_points': [(500, 100), (300, 700), (700, 700), (350, 600), (650, 600)],
'connections': [(1, 3), (1, 2), (2, 4), (0, 3), (0, 4)]
},
'Oph': {
'name': 'Ophiuchus',
'star_points': [(500, 100), (300, 300), (700, 300), (200, 500), (800, 500), (300, 700), (700, 700), (500, 900)],
'connections': [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 7)]
},
'Peg': {
'name': 'Pegasus',
'star_points': [(200, 200), (800, 200), (200, 800), (800, 800), (500, 500), (100, 500), (500, 100)],
'connections': [(0, 1), (1, 3), (3, 2), (2, 0), (2, 4), (4, 5), (1, 6)]
},
'Per': {
'name': 'Perseus',
'star_points': [(500, 200), (600, 400), (700, 600), (500, 700), (300, 600), (400, 400), (200, 300)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (5, 6)]
},
'Sge': {
'name': 'Sagitta',
'star_points': [(300, 500), (700, 500), (500, 300), (500, 700)],
'connections': [(0, 2), (1, 2), (2, 3)]
},
'Ser': {
'name': 'Serpens',
'star_points': [(200, 800), (300, 600), (400, 400), (500, 600), (600, 800), (700, 600), (800, 400)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6)]
},
'Tri': {
'name': 'Triangulum',
'star_points': [(500, 200), (300, 700), (700, 700)],
'connections': [(0, 1), (1, 2), (2, 0)]
},
'UMa': {
'name': 'Ursa Major',
'star_points': [(868, 153), (738, 252), (585, 230), (453, 314), (298, 289), (170, 381), (118, 217)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]
},
'UMi': {
'name': 'Ursa Minor',
'star_points': [(163, 755), (223, 584), (320, 473), (448, 383), (530, 240), (405, 218), (592, 404)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 3)]
},
'Vul': {
'name': 'Vulpecula',
'star_points': [(200, 800), (400, 600), (600, 400), (800, 200)],
'connections': [(0, 1), (1, 2), (2, 3)]
},
# =====================================================
# SOUTHERN HEMISPHERE CONSTELLATIONS
# =====================================================
'Ant': {
'name': 'Antlia',
'star_points': [(353, 335), (523, 239)],
'connections': [(0, 1)]
},
'Aps': {
'name': 'Apus',
'star_points': [(244, 342), (426, 363), (530, 219), (344, 182)],
'connections': [(0, 1), (1, 2), (2, 3), (1, 3)]
},
'Ara': {
'name': 'Ara',
'star_points': [(500, 200), (450, 300), (550, 300), (500, 400), (400, 500), (600, 500)],
'connections': [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
},
'Cae': {
'name': 'Caelum',
'star_points': [(500, 500), (400, 400)],
'connections': [(0, 1)]
},
'Car': {
'name': 'Carina',
'star_points': [(100, 500), (300, 400), (400, 600), (600, 550), (700, 350), (500, 200), (250, 250)],
'connections': [(0, 1), (1, 2), (1, 6), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)]
},
'Cen': {
'name': 'Centaurus',
'star_points': [(100, 600), (200, 400), (400, 300), (600, 400), (700, 600), (500, 500), (300, 500), (400, 700), (500, 800), (300, 850)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (1, 6), (6, 5), (5, 7), (7, 8), (8, 9)]
},
'Cet': {
'name': 'Cetus',
'star_points': [(800, 200), (650, 300), (500, 400), (300, 450), (200, 600), (400, 700), (550, 600)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 2)]
},
'Cha': {
'name': 'Chamaeleon',
'star_points': [(200, 200), (300, 400), (500, 500), (400, 300)],
'connections': [(0, 1), (1, 2), (0, 3)]
},
'Cir': {
'name': 'Circinus',
'star_points': [(500, 300), (300, 500), (500, 700)],
'connections': [(0, 1), (1, 2), (2, 0)]
},
'CMa': {
'name': 'Canis Major',
'star_points': [(500, 200), (300, 400), (400, 600), (550, 700), (700, 600), (600, 400)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 5)]
},
'CMi': {
'name': 'Canis Minor',
'star_points': [(400, 600), (600, 400)],
'connections': [(0, 1)]
},
'Col': {
'name': 'Columba',
'star_points': [(400, 300), (600, 400), (500, 600), (300, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0)]
},
'CrA': {
'name': 'Corona Australis',
'star_points': [(200, 500), (400, 450), (600, 500), (500, 600), (300, 600)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
},
'Crt': {
'name': 'Crater',
'star_points': [(200, 400), (400, 450), (500, 350), (300, 300)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0)]
},
'Cru': {
'name': 'Crux',
'star_points': [(500, 100), (500, 800), (200, 500), (800, 500)],
'connections': [(0, 1), (2, 3)]
},
'Crv': {
'name': 'Corvus',
'star_points': [(200, 500), (400, 500), (400, 300), (200, 300), (500, 600)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0), (1, 4)]
},
'Dor': {
'name': 'Dorado',
'star_points': [(200, 600), (400, 500), (600, 400)],
'connections': [(0, 1), (1, 2)]
},
'Eri': {
'name': 'Eridanus',
'star_points': [(200, 100), (300, 200), (250, 300), (350, 400), (300, 500), (400, 600), (500, 700), (600, 800), (700, 900)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)]
},
'For': {
'name': 'Fornax',
'star_points': [(400, 300), (600, 400), (500, 600)],
'connections': [(0, 1), (0, 2)]
},
'Gru': {
'name': 'Grus',
'star_points': [(500, 200), (400, 400), (600, 400), (500, 600), (500, 800)],
'connections': [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
},
'Hor': {
'name': 'Horologium',
'star_points': [(300, 200), (500, 300), (600, 500), (400, 700), (200, 600)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4)]
},
'Hya': {
'name': 'Hydra',
'star_points': [(100, 400), (200, 300), (300, 400), (400, 500), (500, 600), (600, 700), (700, 600), (800, 500), (900, 400)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)]
},
'Hyi': {
'name': 'Hydrus',
'star_points': [(200, 800), (500, 600), (800, 200)],
'connections': [(0, 1), (1, 2)]
},
'Ind': {
'name': 'Indus',
'star_points': [(300, 200), (700, 400), (500, 700)],
'connections': [(0, 1), (0, 2)]
},
'Lep': {
'name': 'Lepus',
'star_points': [(400, 300), (600, 300), (600, 500), (400, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0)]
},
'Lup': {
'name': 'Lupus',
'star_points': [(200, 300), (400, 200), (600, 300), (500, 500), (300, 500), (400, 700)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (3, 5)]
},
'Men': {
'name': 'Mensa',
'star_points': [(200, 700), (800, 700), (700, 300), (300, 300)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0)]
},
'Mic': {
'name': 'Microscopium',
'star_points': [(300, 700), (700, 700), (600, 300), (400, 300)],
'connections': [(0, 1), (1, 2), (2, 3)]
},
'Mon': {
'name': 'Monoceros',
'star_points': [(200, 700), (500, 500), (800, 300)],
'connections': [(0, 1), (1, 2)]
},
'Mus': {
'name': 'Musca',
'star_points': [(300, 300), (700, 300), (500, 600), (200, 700), (800, 700)],
'connections': [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4)]
},
'Nor': {
'name': 'Norma',
'star_points': [(300, 700), (700, 600), (600, 200), (200, 300)],
'connections': [(0, 1), (1, 2), (3, 0)]
},
'Oct': {
'name': 'Octans',
'star_points': [(500, 200), (200, 500), (800, 500)],
'connections': [(0, 1), (0, 2)]
},
'Ori': {
'name': 'Orion',
'star_points': [(202, 185), (715, 843), (121, 217), (797, 811), (423, 495), (473, 513), (524, 529)],
'connections': [(0, 2), (0, 4), (1, 3), (1, 6), (2, 4), (3, 6), (4, 5), (5, 6)]
},
'Pav': {
'name': 'Pavo',
'star_points': [(500, 200), (300, 400), (200, 600), (300, 800), (500, 700), (700, 500)],
'connections': [(0, 1), (1, 2), (1, 5), (2, 3), (3, 4), (4, 5)]
},
'Phe': {
'name': 'Phoenix',
'star_points': [(500, 200), (300, 400), (200, 600), (400, 800), (600, 700), (700, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
},
'Pic': {
'name': 'Pictor',
'star_points': [(200, 700), (500, 500), (800, 300)],
'connections': [(0, 1), (1, 2)]
},
'PsA': {
'name': 'Piscis Austrinus',
'star_points': [(500, 200), (400, 400), (300, 600), (500, 700), (700, 600), (600, 400)],
'connections': [(0, 1), (0, 5), (1, 2), (2, 3), (3, 4), (4, 5)]
},
'Pup': {
'name': 'Puppis',
'star_points': [(200, 300), (400, 200), (600, 300), (500, 500), (300, 500), (400, 700)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (2, 5)]
},
'Pyx': {
'name': 'Pyxis',
'star_points': [(300, 700), (500, 500), (700, 300)],
'connections': [(0, 1), (1, 2)]
},
'Ret': {
'name': 'Reticulum',
'star_points': [(300, 300), (700, 300), (700, 700), (300, 700)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 0)]
},
'Scl': {
'name': 'Sculptor',
'star_points': [(200, 800), (400, 600), (600, 400), (800, 200)],
'connections': [(0, 1), (1, 2), (2, 3)]
},
'Sct': {
'name': 'Scutum',
'star_points': [(500, 200), (300, 400), (500, 600), (700, 400)],
'connections': [(0, 1), (0, 3), (1, 2), (3, 2)]
},
'Sex': {
'name': 'Sextans',
'star_points': [(300, 700), (500, 500), (700, 300)],
'connections': [(0, 1), (1, 2)]
},
'Tel': {
'name': 'Telescopium',
'star_points': [(300, 700), (700, 500), (500, 200)],
'connections': [(0, 1), (1, 2)]
},
'TrA': {
'name': 'Triangulum Australe',
'star_points': [(500, 200), (200, 700), (800, 700)],
'connections': [(0, 1), (1, 2), (2, 0)]
},
'Tuc': {
'name': 'Tucana',
'star_points': [(500, 200), (300, 400), (200, 600), (400, 800), (700, 700), (600, 500)],
'connections': [(0, 1), (1, 2), (2, 3), (0, 5), (4, 5)]
},
'Vel': {
'name': 'Vela',
'star_points': [(200, 300), (400, 200), (600, 300), (500, 500), (300, 500), (400, 700)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 3)]
},
'Vol': {
'name': 'Volans',
'star_points': [(200, 300), (400, 200), (600, 300), (500, 500), (300, 500), (400, 700)],
'connections': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 4)]
}
}

def get_yolo_detections(model_path: str, 
                        image_path: str, 
                        yaml_path: str,
                        conf_threshold: float = 0.25) -> dict:
    print(f"--- Running inference on: {os.path.basename(image_path)} ---")
    
    # --- 1. Input Validation ---
    for path in [model_path, image_path, yaml_path]:
        if not os.path.exists(path):
            print(f"ERROR: File not found at '{path}'")
            return {}

    detections_dict = defaultdict(list)

    try:
        # --- 2. Load Class Names and Model ---
        with open(yaml_path, 'r') as f:
            class_names = yaml.safe_load(f)['names']
        
        model = YOLO(model_path)

        # --- 3. Run Prediction ---
        # The verbose=False argument suppresses detailed console output
        results = model.predict(source=image_path, conf=conf_threshold, verbose=False)
        
        # The 'results' object is a list, we process the first (and only) result
        result = results[0]
        
        # --- 4. Extract and Format Detections ---
        # Get the class indices of all detections
        detected_class_indices = result.boxes.cls.tolist()
        
        # Get the normalized bounding box coordinates [x_center, y_center, width, height]
        normalized_bboxes = result.boxes.xywhn.tolist()

        if len(detected_class_indices) == 0:
            print("No objects were detected in this image.")
            return {}

        for i, class_index in enumerate(detected_class_indices):
            label_name = class_names[int(class_index)]
            normalized_bbox = normalized_bboxes[i]
            detections_dict[label_name].append(normalized_bbox)
        
        print("✅ Inference complete.")
        return dict(detections_dict)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

# =====================================================
# UTILS
# =====================================================
def denormalize_box_from_center(normalized_box, img_w, img_h):
    x_center_rel, y_center_rel, w_rel, h_rel = normalized_box
    w, h = int(w_rel * img_w), int(h_rel * img_h)
    x_center, y_center = int(x_center_rel * img_w), int(y_center_rel * img_h)
    x, y = x_center - (w // 2), y_center - (h // 2)
    return [x, y, w, h]

# =====================================================
# STAR DETECTION 
# =====================================================
def find_stars_within_box(image, constellation_box, expected_star_count):
    x, y, w, h = constellation_box
    roi = image[y:y+h, x:x+w]
    if roi.size == 0: return []
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    threshold_levels = [150, 130, 110, 90, 70, 50]
    for thresh_val in threshold_levels:
        _ , binary_roi = cv2.threshold(gray_roi, thresh_val, 255, cv2.THRESH_BINARY)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_roi, connectivity=8)
        current_pass_stars = []
        if num_labels > 1:
            for i in range(1, num_labels):
                area = stats[i, cv2.CC_STAT_AREA]
                if area >= 5:
                    cx, cy = centroids[i]
                    global_coord = (x + int(cx), y + int(cy))
                    current_pass_stars.append({'coord': global_coord, 'area': area})
        if len(current_pass_stars) >= expected_star_count:
            current_pass_stars.sort(key=lambda s: s['area'], reverse=True)
            top_stars = current_pass_stars[:expected_star_count]
            return [star['coord'] for star in top_stars]
    return []

# =====================================================
# THE DEFINITIVE, CORRECTED STAR MAPPER (Procrustes with Reflection Fix)
# =====================================================
def map_and_order_stars(canonical_model, detected_points):
    """
    Definitive mapping using Procrustes analysis, with a critical fix
    to prevent reflection errors (mirror images).
    """
    canonical_points = np.array(canonical_model['star_points'], dtype=float)
    if len(detected_points) != len(canonical_points): return None
    detected_points = np.array(detected_points, dtype=float)

    # --- Step 1: Center both point sets ---
    canonical_center = np.mean(canonical_points, axis=0)
    detected_center = np.mean(detected_points, axis=0)
    canonical_centered = canonical_points - canonical_center
    detected_centered = detected_points - detected_center

    # --- Step 2: Find optimal rotation using SVD ---
    covariance_matrix = np.dot(detected_centered.T, canonical_centered)
    U, S, Vt = np.linalg.svd(covariance_matrix)
    rotation = np.dot(Vt.T, U.T)
    
    # --- Step 3: THE CRITICAL FIX - Check for and correct reflection ---
    # If the determinant of the rotation matrix is negative, it's a reflection, not a true rotation.
    # We fix this by flipping the last singular vector.
    if np.linalg.det(rotation) < 0:
        Vt_corrected = Vt.copy()
        Vt_corrected[-1,:] *= -1
        rotation = np.dot(Vt_corrected.T, U.T)

    # --- Step 4: Apply the corrected rotation ---
    detected_aligned = np.dot(detected_centered, rotation)

    # --- Step 5: Find the best point-to-point pairing ---
    cost_matrix = cdist(canonical_centered, detected_aligned)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # --- Step 6: Reconstruct the ordered list ---
    ordered_points = [None] * len(detected_points)
    for r, c in zip(row_ind, col_ind):
        ordered_points[r] = tuple(map(int, detected_points[c]))
        
    print("    [Mapping Success] Correctly ordered stars using Procrustes analysis with reflection correction.")
    return ordered_points

# =====================================================
# DRAWING
# =====================================================
def draw_constellation(image, ordered_star_coords, canonical_model):
    if not ordered_star_coords: return
    for connection in canonical_model['connections']:
        start, end = ordered_star_coords[connection[0]], ordered_star_coords[connection[1]]
        cv2.line(image, start, end, (128, 0, 128), 3)
    for pt in ordered_star_coords:
        cv2.circle(image, pt, 5, (0, 165, 255), -1)
    cv2.putText(image, canonical_model['name'], (ordered_star_coords[0][0] - 20, ordered_star_coords[0][1] - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2)

# =====================================================
# MAIN
# =====================================================
# --- THIS IS THE NEW "MAIN" FUNCTION FOR OUR PIPELINE ---
# Add this code to the VERY END of pipeline.py


# In pipeline.py, replace the old run_full_pipeline function with this one

def run_full_pipeline(image_path: str, model_path: str, yaml_path: str, output_path: str) -> bool:
    """
    Coordinates the entire detection and drawing pipeline.
    Returns: True if an image was successfully created, False otherwise.
    """
    # 1. Run YOLO to get the constellation's bounding box
    detected_objects = get_yolo_detections(
        model_path=model_path,
        image_path=image_path,
        yaml_path=yaml_path
    )
    
    if not detected_objects:
        print("Pipeline stopped: YOLO did not detect any constellations.")
        return False
        
    img = cv2.imread(image_path)
    if img is None: return False
    
    img_h, img_w, _ = img.shape
    
    # 2. Iterate through each detected constellation
    for label, normalized_boxes in detected_objects.items():
        # --- THIS IS THE CORRECTED LOGIC ---
        # The 'label' from YOLO (e.g., 'Cyg') is the key we need for CONSTELLATION_DATA
        cnn_label = label 
        
        if cnn_label not in CONSTELLATION_DATA:
            print(f"Warning: Detected '{label}' but no matching key in CONSTELLATION_DATA.")
            continue
        # ------------------------------------

        normalized_box = normalized_boxes[0]
        constellation_box = denormalize_box_from_center(normalized_box, img_w, img_h)
        canonical_model = CONSTELLATION_DATA[cnn_label]
        
        detected_points = find_stars_within_box(img, constellation_box, expected_star_count=len(canonical_model['star_points']))
        
        if len(detected_points) == len(canonical_model['star_points']):
            ordered_points = map_and_order_stars(canonical_model, detected_points)
            if ordered_points:
                draw_constellation(img, ordered_points, canonical_model)
        else:
            print(f"Skipping '{label}': Found {len(detected_points)} of {len(canonical_model['star_points'])} required stars.")

    # 6. Save the final image
    cv2.imwrite(output_path, img)
    print(f"✅ Pipeline complete. Output saved to {output_path}")
    return True