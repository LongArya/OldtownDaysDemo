import pygame
import os
import sys
import numpy as np
from game_enums.achievements_names import AchievementsNames
from game_enums.user_intention import UserIntention
from responsive_objects.slide import Slide
from responsive_objects.achievement_button import AchievementButton
from responsive_objects.mouse_responsive import MouseResponsive
from game_constants import ACHIEVEMENTS_DIR


# todo add meshgrid for the small icons positions
class AchievementPanel(MouseResponsive, Slide):
    def __init__(self, screen_w, screen_h):
        super().__init__(0)
        # parameters for counting buttons drawing positions
        self._screen_w = screen_w
        self._screen_h = screen_h
        self._ach_w = 80
        self._ach_h = 80
        self._x_offset = 20
        self._y_offset = 20
        self._x_start = 50
        self._y_start = 50
        self._buttons_drawing_positions = self._get_drawing_positions()
        self._big_icon_active_pos = (200, 175)
        self._description_pos = (447, 175)
        self._buttons = self._load_buttons()
        self._ach_state = self._get_achievements_state(0)  # fixme dummy implementation without achievement manager
        self._spectating_button = -1

    def _get_drawing_positions(self):
        x_stop = self._screen_w - self._ach_w - self._x_offset
        x = np.arange(self._x_start, x_stop + 1, self._ach_w + self._x_offset)
        y_stop = self._screen_h - self._ach_h - self._y_offset
        y = np.arange(self._y_start, y_stop + 1, self._ach_h + self._y_offset)
        xx, yy = np.meshgrid(x, y)
        coord = np.vstack((xx.flatten(), yy.flatten())).T
        return coord

    def _load_buttons(self):
        """returns list of buttons"""  # fixme kind of obvious do we even need this
        buttons = []
        for index, a in enumerate(AchievementsNames):
            ach_dir = os.path.join(ACHIEVEMENTS_DIR, a.name)
            if os.path.exists(ach_dir):
                print(f'LOAD ACHIEVEMNT FROM {ach_dir}')
                small_icon_locked = pygame.image.load(os.path.join(ach_dir, 'SmallIconGs.png'))
                small_icon_unlocked = pygame.image.load(os.path.join(ach_dir, 'SmallIcon.png'))
                big_icon_locked = pygame.image.load(os.path.join(ach_dir, 'BigIconGs.png'))
                big_icon_unlocked = pygame.image.load(os.path.join(ach_dir, 'BigIcon.png'))
                description = pygame.image.load(os.path.join(ach_dir, 'Description.png'))
                button = AchievementButton(a.name,
                                           small_icon_locked,
                                           small_icon_unlocked,
                                           big_icon_locked,
                                           big_icon_unlocked,
                                           description,
                                           self._buttons_drawing_positions[index],
                                           self._big_icon_active_pos,
                                           self._description_pos,
                                           0)
                buttons.append(button)
        return buttons

    # todo later implement interaction with achievement manager
    def _get_achievements_state(self, achievement_manager):
        dummy_dict = {}
        for a in AchievementsNames:
            dummy_dict[a.name] = True
        return dummy_dict

    def update(self):
        """ track which button was pressed and assign it to be spectated:
        it is should be tracked because it is should be drawn last. every mouse pressing menas that whatever 
        button was in spectative mode it should exit it"""   # fixme refine this string
        # if no button is in spectator mode check if some button is pressed
        if self._spectating_button == -1:
            for index, button in enumerate(self._buttons):
                if button.get_user_intention_and_update_track() == UserIntention.SWITCH_ON:
                    self._spectating_button = index
        # else every pressing is considered to be exit out of spectator mod
        else:
            if self.get_user_intention_and_update_track() == UserIntention.SWITCH_ON:
                self._spectating_button = -1

    def draw(self, screen):
        for index, button in enumerate(self._buttons):
            ach_name = button.achievement_name
            button.draw_idle(screen, self._ach_state[ach_name])
        if self._spectating_button != -1:
            ach_name = self._buttons[self._spectating_button].achievement_name
            self._buttons[self._spectating_button].draw_description(screen, self._ach_state[ach_name])


if __name__ == '__main__':
    pygame.init()
    p = AchievementPanel(1200, 680)
    coord = p._buttons_drawing_positions
    width, height = 1200, 680
    black = (255, 255, 255)
    size = (width, height)
    screen = pygame.display.set_mode(size)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(black)
        p.update()
        p.draw(screen)
        pygame.display.flip()
