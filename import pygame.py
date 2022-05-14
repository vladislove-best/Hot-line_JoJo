import pygame as pg
pg.init()

class Player(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.move_speed = 7
		self.xvel = 0
		self.yvel = 0
		self.width = 32
		self.height = 32
		self.Color = '#f5f5dc'
		self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
		self.startY = y
		self.image = pg.Surface((self.width,self.height))
		self.image.fill(pg.Color(self.Color))
		self.rect = pg.Rect(x, y, self.width, self.height)
	def update(self, left, right, up, down):
		if left:
			self.xvel = -self.move_speed
		if right:
			self.xvel = self.move_speed
		if down:
			self.yvel = self.move_speed
		if up:
			self.yvel = -self.move_speed 

		if not(left or right):
			self.xvel = 0
		if not(up or down):
			self.yvel = 0

		self.rect.x += self.xvel
		self.rect.y += self.yvel
	def draw(self, window):
		window.blit(self.image, (self.rect.x,self.rect.y))

display_width = int(960)
display_heigth = int(640)
display = (display_width, display_heigth)
bg_c = "#004400"
window = pg.display.set_mode(display)
bg = pg.Surface((display_width,display_heigth))
bg.fill(pg.Color(bg_c))
wall_width = 32
wall_height = 32
wall_c = '#808080'
FPS = 60
clock = pg.time.Clock()
left=right=up=down=False
hero = Player(896,576)
level = [
       "------------------------------",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                            -",
       "-                    ---------",
       "-                    -       -",
       "-                    -       -",
       "-                            -",
       "-                            -",
       "------------------------------"]


running = 1
while running == 1:
	clock.tick(FPS)
	for e in pg.event.get(): 
		if e.type == pg.QUIT:
			running = 0
		if e.type == pg.KEYDOWN:
			if e.key == pg.K_a:
				left = True
			if e.key == pg.K_d:
				right = True
			if e.key == pg.K_w:
				up = True
			if e.key == pg.K_s:
				down = True
		if e.type == pg.KEYUP:
			if e.key == pg.K_a:
				left = False
			if e.key == pg.K_d:
				right = False
			if e.key == pg.K_w:
				up = False
			if e.key == pg.K_s:
				down = False
	hero.update(left, right, up, down)
	window.blit(bg, (0,0))     
	x=y=0 # координаты
	for row in level: # вся строка
		for col in row: # каждый символ
			if col == "-":
				pf = pg.Surface((wall_width,wall_height))
				pf.fill(pg.Color(wall_c)) 
				window.blit(pf,(x,y))
                    
			x += wall_width #блоки платформы ставятся на ширине блоков
		y += wall_height    #то же самое и с высотой
		x = 0
	hero.draw(window)
	pg.display.update()
pg.quit()