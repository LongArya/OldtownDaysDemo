import pygame
import utils
import sys
from link import Link
from droplet import Droplet
from game_constants import DROPLETS_DIR, DROPLET_WIDTH
import os
from game_enums.metals import Metals
pygame.init()


# todo add doc string
class Channel:
	def __init__(self, link):
		self._link = link
		self._link_place = link.rect
		self._droplets = []
		self.intersection_threshold = 1
		self.channel_rect = pygame.Rect(*self._link.rect)
		self.channel_rect.top = 0

	def create_and_set_ball(self, metal):
		half_width = int(self.channel_rect.width / 2)
		drop_x = self.channel_rect.left + half_width - int(DROPLET_WIDTH / 2)
		drop_y = self.channel_rect.top
		img = pygame.image.load(os.path.join(DROPLETS_DIR, f'{metal.name}.png'))
		drop = Droplet(metal, 1, img, (drop_x, drop_y))
		self._droplets.append(drop)

	def link_is_available(self):
		return self._link is not None

	# todo reflect in the name that method counts ruined droplets
	def update(self):
		""" All droplets fall
		Then if droplet is in the place where link should be there is three possible outcomes
		1) There is link and droplet is of the same metal - success
		2) There is link and droplet is of the different metal - droplet is ruined
		3) There is no link - droplet is ruined
		In either way that means droplet doesnt need to be updated anymore/
		Amount of ruined droplets is counted"""
		droplets_ixs_to_discard = []
		ruined_droplets = 0
		for index in range(len(self._droplets)):
			self._droplets[index].fall()
			intersection = utils.get_intersection(self._link_place, self._droplets[index].rect)
			if intersection > self.intersection_threshold:
				droplets_ixs_to_discard.append(index)
				if self._link is None:
					ruined_droplets += 1
				else:
					if self._link.metal == self._droplets[index].metal:
						self._link.pour_metal()
					else:
						ruined_droplets += 1
		self._droplets = [self._droplets[i] for i in range(len(self._droplets)) if i not in droplets_ixs_to_discard]
		if self._link is not None:
			self._link.update()
		return ruined_droplets

	def draw(self, screen):
		for drop in self._droplets:
			drop.draw(screen)
		if self._link is not None:
			self._link.draw(screen)

	def yield_link(self):
		link = self._link
		self._link = None
		return link

	def set_link(self, link):
		self._link = link


if __name__ == '__main__':
	pygame.init()
	from game_constants import LINKS_DIR
	# empty , full, timer, position, time, metal
	m = Metals.GOLD
	gpath = os.path.join(LINKS_DIR, m.name)
	empty = pygame.image.load(os.path.join(gpath, 'Empty.png'))
	full = pygame.image.load(os.path.join(gpath, 'Full.png'))
	timer = pygame.image.load(os.path.join(gpath, 'FullTimer.png'))
	link = Link(empty, full, timer, (40, 533), 5000, Metals.GOLD)
	p = Channel(link)
	width, height = 1200, 680
	black = (255, 255, 255)
	size = (width, height)
	screen = pygame.display.set_mode(size)

	ttl = 1500
	clock = pygame.time.Clock()
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				sys.exit()
		screen.fill(black)
		ttl -= clock.tick()
		if ttl < 0:
			p.create_and_set_ball(Metals.GOLD)
			ttl = 100
		p.update()
		p.draw(screen)
		pygame.display.flip()
