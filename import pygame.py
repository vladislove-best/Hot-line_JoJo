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
	def update(self, left, right, up, platforms):
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

		self.rect.y += self.yvel
		self.collide(0, self.yvel, platforms)

		self.rect.x += self.xvel # переносим свои положение на xvel
		self.collide(self.xvel, 0, platforms)
	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if pg.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

				if xvel > 0:                      # если движется вправо
					self.rect.right = p.rect.left # то не движется вправо
	
				if xvel < 0:                      # если движется влево
					self.rect.left = p.rect.right # то не движется влево
		
				if yvel > 0:                      # если падает вниз
					self.rect.bottom = p.rect.top # то не падает вниз
					self.onGround = True          # и становится на что-то твердое
					self.yvel = 0                 # и энергия падения пропадает

				if yvel < 0:                      # если движется вверх
					self.rect.top = p.rect.bottom # то не движется вверх
					self.yvel = 0                 # и энергия прыжка пропадает

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((wall_width, wall_height))
        self.image.fill(pg.Color(wall_c))
        self.rect = pg.Rect(x, y, wall_width, wall_height)

class Camera(object):
	def __init__(self, camera_func, width, height):
		self.camera_func = camera_func
		self.state = pg.Rect(0, 0, width, height)

	def apply(self, target):
		return target.rect.move(self.state.topleft)

	def update(self, target):
		self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+display_width / 2, -t+display_heigth / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-display_width), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-display_heigth), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return pg.Rect(l, t, w, h)      

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
entities = pg.sprite.Group() # Все объекты
platforms = [] # то, во что мы будем врезаться или опираться
entities.add(hero)
level = [
       "--------------------------------------------------------------",
       "-                                                            -",
       "-                                                            -",
       "-                                                            -",
       "-     -                                                      -",
       "-                              -                             -",
       "-              -                                             -",
       "-                                                            -",
       "-                                                            -",
       "-                                                            -",
       "-                              -                             -",
       "-                                                            -",
       "-            -                                               -",
       "-                                                            -",
       "-                                                    ---------",
       "-                               -                    -       -",
       "-                                                    -       -",
       "-                                                            -",
       "-           -                                                -",
       "--------------------------------------------------------------"]

total_level_width  = len(level[0])*wall_width # Высчитываем фактическую ширину уровня
total_level_height = len(level)*wall_height   # высоту
camera = Camera(camera_configure, total_level_width, total_level_height)
running = 1
y=0
for row in level: # вся строка
	x = 0
	for col in row: # каждый символ
		if col == "-":
			pf = Platform(x,y)
			entities.add(pf)
			platforms.append(pf)
       
		x += wall_width #блоки платформы ставятся на ширине блоков
	y += wall_height    #то же самое и с высотой
total_level_width  = len(level[0])*wall_width # Высчитываем фактическую ширину уровня
total_level_height = len(level)*wall_height   # высоту
   
camera = Camera(camera_configure, total_level_width, total_level_height)
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
	hero.update(left, right, up, platforms)
	window.blit(bg, (0,0))     
	x=y=0 # координаты
	for row in level: # вся строка
		for col in row: # каждый символ
			if col == "-":
				pf = Platform(x,y)
				entities.add(pf)
				platforms.append(pf)
                    
			x += wall_width #блоки платформы ставятся на ширине блоков
		y += wall_height    #то же самое и с высотой
		x = 0
	camera.update(hero) # центризируем камеру относительно персонажа
	for e in entities:
		window.blit(e.image, camera.apply(e))
	pg.display.update()
pg.quit()