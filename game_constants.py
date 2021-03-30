import os
from game_enums.metals import Metals
from game_enums.coins_kinds import CoinsKinds
from game_enums.achievements_names import AchievementsNames
from game_enums.game_state import GameState
import pygame
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__)
RESOURSES_DIR = os.path.join(SCRIPT_DIR, 'resourses')
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 680
DROPLET_WIDTH = 30
DROPLET_HEIGHT = 30
LINK_WIDTH = 172
LINK_HEIGHT = 114
ACH_WIDTH = 80
ACH_HEIGHT = 80
LVL_ICON_WIDTH = 80
LVL_ICON_HEIGHT = 80
# RESOURSES CONST
ACHIEVEMENTS_DIR = os.path.join(RESOURSES_DIR, 'Achievements')
DROPLETS_DIR = os.path.join(RESOURSES_DIR, 'Droplets')
LVL_BUTTONS_DIR = os.path.join(RESOURSES_DIR, 'LvlButtons')
BACKGROUNDS_DIR = os.path.join(RESOURSES_DIR, 'Backgrounds')

# GAME CONSTANTS
MOUSE_KEY = 0
LINKS_SWAP_THRD = 0.2
DROPLET_LINK_INTERSECTION_THRD = 1

USER_EVENT_NUM = 1


def generate_event():
    """returns new event keeping track of event num"""
    global USER_EVENT_NUM
    event = pygame.event.Event(pygame.USEREVENT + USER_EVENT_NUM)
    USER_EVENT_NUM += 1
    return event


# Events
# fixme maybe events should be in special file I'll sleep on that
GENERATE_COIN_EVENT = generate_event()
GENERATE_DROP_EVENT = generate_event()
RUINED_DROP_EVENT = generate_event()

LINK_METAL_EVENT_DICT = {}
for m in Metals:
    LINK_METAL_EVENT_DICT[m] = generate_event()
EVENT_TYPE_METAL_DICT = {}
for metal, event in LINK_METAL_EVENT_DICT.items():
    EVENT_TYPE_METAL_DICT[event.type] = metal
LINK_IS_DONE_EVENTS_TYPES = tuple(t for t in EVENT_TYPE_METAL_DICT.keys())

NO_LINK_RUIN_DICT = {}
for m in Metals:
    NO_LINK_RUIN_DICT[m] = generate_event()
EVENT_TYPE_NO_LINK_RUIN_METAL_DICT = {}
for metal, event in NO_LINK_RUIN_DICT.items():
    EVENT_TYPE_NO_LINK_RUIN_METAL_DICT[event.type] = metal
NO_LINK_RUIN_TYPES = tuple(t for t in EVENT_TYPE_NO_LINK_RUIN_METAL_DICT.keys())

LVL_EVENTS_TYPES = (GENERATE_COIN_EVENT.type,
                    GENERATE_DROP_EVENT.type,
                    RUINED_DROP_EVENT.type) + LINK_IS_DONE_EVENTS_TYPES + NO_LINK_RUIN_TYPES

# backgrounds images
LVL_BACKGROUND = pygame.image.load(os.path.join(BACKGROUNDS_DIR, 'Level_background.png'))


# test link fill event
ACHIEVEMENTS_IMAGES = {}
for achievement in AchievementsNames:
    ach_dir = os.path.join(ACHIEVEMENTS_DIR, achievement.name)
    if os.path.exists(ach_dir):
        print(f'LOAD ACHIEVEMNT FROM {ach_dir}')
        small_icon_locked = pygame.image.load(os.path.join(ach_dir, 'SmallIconGs.png'))
        small_icon_unlocked = pygame.image.load(os.path.join(ach_dir, 'SmallIcon.png'))
        big_icon_locked = pygame.image.load(os.path.join(ach_dir, 'BigIconGs.png'))
        big_icon_unlocked = pygame.image.load(os.path.join(ach_dir, 'BigIcon.png'))
        description = pygame.image.load(os.path.join(ach_dir, 'Description.png'))
        ACHIEVEMENTS_IMAGES[achievement] = [small_icon_locked,
                                          small_icon_unlocked,
                                          big_icon_locked,
                                          big_icon_unlocked,
                                          description]


MODE_SELECTION_BUTTONS_INFO = {}
mode_buttons_folder = os.path.join(RESOURSES_DIR, 'Mode_selection')
selection_positions = [[0, 0], [int(SCREEN_WIDTH / 2), 0]]
for state, pos in zip([GameState.INFINITE_PLAY, GameState.LEVEL_CHOOSING], selection_positions):
    folder = os.path.join(mode_buttons_folder, state.name)
    idle_image = pygame.image.load(os.path.join(folder, 'idle.png'))
    active_image = pygame.image.load(os.path.join(folder, 'selected.png'))
    images = [idle_image, active_image]
    MODE_SELECTION_BUTTONS_INFO[state] = {"images": images, "position": pos}


FATHERS_JUDGEMENT_THRD = 0.5
FATHERS_PUNISHMENT = 100  # amount of coins to be disposed of
TRIAL_BONUSES_IMAGES = {}
"""
structure is:
bonus_name:
    - roll image
    - with_description.png
"""


LVL_BUTTONS_IMAGES = []
locked_level_button = pygame.image.load(os.path.join(LVL_BUTTONS_DIR, 'LvlCloseIcon.png'))
for folder_name in sorted(os.listdir(LVL_BUTTONS_DIR)):
    folder_path = os.path.join(LVL_BUTTONS_DIR, folder_name)
    if not os.path.isdir(folder_path):
        continue
    idle_image = pygame.image.load(os.path.join(folder_path, 'idle.png'))
    selected_image = pygame.image.load(os.path.join(folder_path, 'selected.png'))
    LVL_BUTTONS_IMAGES.append([locked_level_button, idle_image, selected_image])



# Challenge
CHALLENGE_TARGET_RADIUS = 30
CHALLENGE_TIMER_LINE_WIDTH = 20
CHALLENGE_FOLDER = os.path.join(RESOURSES_DIR, 'Challenge')
CHALLENGE_IMAGES = {}
""" 
expected challenge folder structure
- metal_key
    background_image.png
    - 001 
        - trace_image.png
        - idle_image.png
        - calling_image.png
    - 002
        - trace_image.png
        - idle_image.png
        - calling_image.png
    ....
....    
"""

for metal in Metals:
    curr_info_dict = {}
    challenge_sub_folder = os.path.join(CHALLENGE_FOLDER, metal.name)
    if not os.path.exists(challenge_sub_folder):
        continue
    bg_img = pygame.image.load(os.path.join(challenge_sub_folder, 'background_image.png'))
    curr_info_dict['bg_img'] = bg_img

    targets_sub_folders = sorted(os.path.join(challenge_sub_folder, f) for f in os.listdir(challenge_sub_folder))
    targets_sub_folders = filter(lambda path: os.path.isdir(path), targets_sub_folders)
    targets_images = []
    for target_folder in targets_sub_folders:
        trace_image_path = os.path.join(target_folder, 'trace_image.png')
        idle_image_path = os.path.join(target_folder, 'idle_image.png')
        calling_image_path = os.path.join(target_folder, 'calling_image.png')
        curr_images = [pygame.image.load(trace_image_path),
                       pygame.image.load(idle_image_path),
                       pygame.image.load(calling_image_path)]
        targets_images.append(curr_images)
    curr_info_dict['targets_images'] = targets_images
    CHALLENGE_IMAGES[metal] = curr_info_dict

# Links
LINKS_DIR = os.path.join(RESOURSES_DIR, 'Links')
"""
Links dir structure:
Links:
    Metal:
        Empty.png
        Full.png
        FullTimer.png
    Metal2
        ...
    ...
"""

LINKS_IMAGES = {}
for metal in Metals:
    link_dir = os.path.join(LINKS_DIR, metal.name)
    if not os.path.exists(link_dir):
        continue
    empty_img_path = os.path.join(link_dir, 'Empty.png')
    full_img_path = os.path.join(link_dir, 'Full.png')
    timer_img_path = os.path.join(link_dir, 'FullTimer.png')
    LINKS_IMAGES[metal] = [pygame.image.load(empty_img_path),
                           pygame.image.load(full_img_path),
                           pygame.image.load(timer_img_path)]

# for each number of links there is special coordinates arrangements ()
links_y = 533
five_links_x = np.arange(5) * 212 + 40
five_links_arrangement = np.vstack((five_links_x, np.ones((5,)) * links_y)).T.astype(np.int32)
LINKS_COORDINATES = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: five_links_arrangement
}


DROPLETS_IMAGES = {}
for metal in Metals:
    droplet_path = os.path.join(DROPLETS_DIR, f'{metal.name}.png')
    if not os.path.exists(droplet_path):
        continue
    DROPLETS_IMAGES[metal] = pygame.image.load(droplet_path)


# Load coins images
COINS_FOLDER = os.path.join(RESOURSES_DIR, "Coins")
COINS_IMAGES = {}
for coin_kind in CoinsKinds:
    COINS_IMAGES[coin_kind] = pygame.image.load(os.path.join(COINS_FOLDER, f'{coin_kind.name}.png'))


COINS_RADIUS = 35
COINS_WIDTH = 70
COINS_HEIGHT = 70
COINS_EDGE_OFFSET = 100
COINS_X_BOUNDARIES = (COINS_WIDTH + COINS_EDGE_OFFSET, SCREEN_WIDTH - COINS_EDGE_OFFSET)
COINS_Y_BOUNDARIES = (COINS_HEIGHT + COINS_EDGE_OFFSET, links_y - COINS_EDGE_OFFSET)
