import pygame
import random
pygame.init()
pygame.mixer.init()

# Thanks to https://minecraft.wiki
# Sounds
zombie_spawn = pygame.mixer.Sound('zombie_sound.mp3')
zombie_hurt1 = pygame.mixer.Sound('zombie_hurt1_sound.ogg')
zombie_hurt2 = pygame.mixer.Sound('zombie_hurt2_sound.ogg')
zombie_death = pygame.mixer.Sound('zombie_death_sound.ogg')

creeper_hiss = pygame.mixer.Sound('creeper_hiss.mp3')
creeper_boom = pygame.mixer.Sound('explode.ogg')
creeper_hurt = pygame.mixer.Sound('creeper_hurt.ogg')
creeper_death = pygame.mixer.Sound('creeper_death.ogg')

spider_death = pygame.mixer.Sound('spider_death.ogg')
spider_hurt = pygame.mixer.Sound('spider_hurt.ogg')
spider_step = pygame.mixer.Sound('spider_step.ogg')

player_hurt = pygame.mixer.Sound('player_hit.mp3')
arrow_fired = pygame.mixer.Sound('arrow_fired.ogg')


song = pygame.mixer.Sound('haggstrom.ogg')
# Setup
w = 400*2.5
h = 300*2.5
screen = pygame.display.set_mode([w, h])
clock = pygame.time.Clock()

# Mobs
z = pygame.image.load('z.png')
z = pygame.transform.scale(z, (236*w/1400, 343*w/1400))
zh = pygame.image.load('zh.png')
zh = pygame.transform.scale(zh, (236*w/1400, 343*w/1400))

c = pygame.image.load('c.png')
c = pygame.transform.scale(c, (300*w/1700, 400*w/1700))
cf = pygame.image.load('cf.png')
cf = pygame.transform.scale(cf, (300*w/1700, 400*w/1700))
ch = pygame.image.load('ch.png')
ch = pygame.transform.scale(ch, (300*w/1700, 400*w/1700))


zc = pygame.image.load('z+c.png')
zc = pygame.transform.scale(zc, (216*w/1500, 339*w/1500))
zch = pygame.image.load('zch.png')
zch = pygame.transform.scale(zch, (216*w/1500, 339*w/1500))

sp = pygame.image.load('spider.png')
sp = pygame.transform.scale(sp, (381*w/2150, 283*w/2150))
sph = pygame.image.load('sph.png')
sph = pygame.transform.scale(sph, (381*w/2100, 283*w/2100))


boom = pygame.image.load('boom.png')
boom = pygame.transform.scale(boom, (500*w/1600, 500*w/1600))

# Players
st = pygame.image.load('steve.png')
st = pygame.transform.scale(st, (157*w/1200, 277*w/1200))

sth = pygame.image.load('sth.png')
sth = pygame.transform.scale(sth, (157*w/1200, 277*w/1200))

# Arrow
ar = pygame.image.load('arrow.png')
ar = pygame.transform.scale(ar, (170*w/1800, 46*w/1800))
# Land
land = pygame.image.load('land.png')
land = pygame.transform.scale(land, (w, h))
land_mask = pygame.mask.from_surface(land)
land_mask_image = land_mask.to_surface()
# HP
heart = pygame.image.load('heart.png')
heart = pygame.transform.scale(heart, (1188*w/(6400*3), 1188*w/(6400*3)))

class Mob:
    def __init__(self, pos, image, speed):
        self.pos = pos
        self.image = image
        self.speed = speed
        self.hp = 4
        if self.image == c:
            self.mob = "c"
        elif self.image == z:
            self.mob = "z"
        elif self.image == zc:
            self.mob = "zc"
        elif self.image == st:
            self.mob = "st"
        elif self.image == sp:
            self.mob = "sp"
            self.hp = 3
        
        
        if self.mob == "st":
            self.hittick = 0
            self.shottick = 0
        # Flip
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            

            
        self.r = self.image.get_rect(topleft = self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.tick = 0
        self.speed_x = 0
        self.speed_y = 0
        
    def draw(self):
        screen.blit(self.image, (self.r.x, self.r.y))
        
    def change(self, image):
        self.image = image
        self.tick = 0
        if self.image == c:
            self.mob = "c"
        elif self.image == cf:
            self.mob = "cf"
        elif self.image == z:
            self.mob = "z"
        elif self.image == zc:
            self.mob = "zc"
        elif self.image == boom:
            self.mob = "boom"
        elif self.image == st:
            self.mob = "st"
        elif self.image == sp:
            self.mob = "sp"
        #Hit images
        elif self.image == ch:
            self.mob = "ch"
        elif self.image == zh:
            self.mob = "zh"
        elif self.image == zch:
            self.mob = "zch"
        elif self.image == sth:
            self.mob = "sth"
        elif self.image == sph:
            self.mob = "sph"
            # Flip
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)
        if self.mask.overlap(land_mask, (-self.r.x, -self.r.y)):
            while self.mask.overlap(land_mask, (-self.r.x, -self.r.y)):
                self.r.y -= 1
            self.r.y += 1
                
    def move(self, amount):
        #print("Start" + str(self.r.x))
        self.r.x += amount
        #print("End" + str(self.r.x))
    def change_amount(self):
        self.r.x += self.speed_x
        self.r.y += self.speed_y
        
        #print(1)
        if self.mask.overlap(land_mask, (-self.r.x, -self.r.y)):
            #print(2)
            self.speed_y = 0
            while self.mask.overlap(land_mask, (-self.r.x, -self.r.y)):
                self.r.y -= 1
            self.r.y += 1
            
        else:
            self.speed_y += w/400
            
        self.speed_x *= 0.9

class Arrow:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction
        
        self.image = ar
        
        if self.direction < 0:
            self.speed_x = -w/40 # -20
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.direction > 0:
            self.speed_x = w/40 # 20
            
        self.speed_y = 0
        
        self.r = self.image.get_rect(topleft=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        self.r.x += self.speed_x
        self.r.y += self.speed_y
        self.speed_y += w/4000 #0.2
        self.speed_x *= 0.99
        
    def draw(self):
        screen.blit(self.image, (self.r.x, self.r.y))
        
running = True

while running:
    mobs = []
    arrows = []
    steve = Mob((w/2, 0.9*h), st, -1)
    steve.hp = 9
    score = 0
    
    game_tick = 0
    fps = 30
    
    level = 1
    rate = 90
    mobs_left = 10+5*level
    level_tick = 0
    
    alive = True
    over = False
    
    while alive:
        screen.fill((0,0,0))
        screen.blit(land, (0,0))

        if game_tick%900 == 0:
            song.play()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                alive = False
                over = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not steve.image == sth and steve.shottick > 10:
                    arrows.append(Arrow((steve.r.x, steve.r.y + 277*w/3600), steve.speed))
                    steve.shottick = 0
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not steve.image == sth and steve.shottick > 10:
                        arrow_fired.play()
                        arrows.append(Arrow((steve.r.x, steve.r.y + 277*w/3600), steve.speed))
                        steve.shottick = 0
                
                
        # Spawn
            
        if game_tick%rate == 0:
            
            if mobs_left == 0: # End of level
                
                if level < 100:
                    level += 1
                if rate >= 5:
                    rate -= 5
                if level <= 10:
                    mobs_left = 10+5*level
                else:
                    mobs_left = 70

                level_tick = 0
                
            elif mobs_left > 0:
                mobs_left -= 1
                
                if random.randint(0, 1) ==  0: # Keep spawning
                    
                    if random.randint(0, 1) == 0:
                        if random.randint(1, 3) == 3:
                            if random.randint(0,1)==0:
                                mobs.append(Mob((0.9*w, 0.9*h), c, -w/800))
                            else:
                                mobs.append(Mob((0.9*w, 0.9*h), sp, -w/150))
                        else:
                            mobs.append(Mob((0.9*w, 0.9*h), z, -w/400))
                            zombie_spawn.play()
                    else:
                        if random.randint(1, 3) == 3:
                            if random.randint(0,1)==0:
                                mobs.append(Mob((0.9*w, 0), c, -w/800))
                            else:
                                mobs.append(Mob((0.9*w, 0), sp, -w/150))
                        else:
                            mobs.append(Mob((0.9*w, 0), z, -w/400))
                            zombie_spawn.play()
                else:
                    if random.randint(0, 1) == 0:
                        if random.randint(1, 3) == 3:
                            if random.randint(0,1)==0:
                                mobs.append(Mob((-w/80, 0.9*h), c, w/800))
                            else:
                                mobs.append(Mob((-w/80, 0.9*h), sp, w/150))
                        else:
                            mobs.append(Mob((-w/80, 0.9*h), z, w/400))
                            zombie_spawn.play()
                    else:
                        if random.randint(1, 3) == 3:
                            if random.randint(0,1)==0:
                                mobs.append(Mob((-w/80, 0), c, w/800))
                            else:
                                mobs.append(Mob((-w/80, 0), sp, w/150))
                        else:
                            mobs.append(Mob((-w/80, 0), z, w/400))
                            zombie_spawn.play()
                            
                        
        for mob in mobs:
            mob.draw()
            mob.change_amount()
            if mob.r.x < -w/8 or mob.r.x > w + w/8:
                mobs.remove(mob)
            
            if mob.mob == "c":
                if mob.tick < 300:
                    mob.move(mob.speed)
                mob.tick += 1
                if mob.tick == 300 or mob.tick == 301:
                    creeper_hiss.play()
                
                # Creeper boom at tick=340


                if mob.tick > 300 and mob.tick%5 == 0:
                    mob.change(cf)
                    
            elif mob.mob == "cf":
                mob.tick += 1
                if mob.tick%5 == 0:
                    if mob.tick < 335:
                        mob.change(c)
                    else:
                        mob.change(boom)
                        mob.r.x -= w/18
                        creeper_boom.play()
                        
            elif mob.mob == "boom":
                mob.tick += 1
                if mob.tick%15 == 0:
                    mobs.remove(mob)
                    
     
            elif mob.mob == "z":
                mob.move(mob.speed)
                for other in mobs:
                    if other.mob == "c" or other.mob == "cf":    
                        if mob.mask.overlap(other.mask, (other.r.x - mob.r.x, other.r.y - mob.r.y)) and other.mask.overlap(land_mask, (-other.r.x, -other.r.y)) and other.speed_y >= 0:
                            mob.change(zc)
                            mob.hp = 6
                            mob.r.y += w/50
                            mobs.remove(other)
            elif mob.mob == "zc":
                mob.tick += 1
                mob.move(mob.speed)
                if mob.tick%15==0:
                    mob.change(z)
                    mob.hp = 3
                    mob.r.y -= w/50
                    item = Mob((mob.r.x, mob.r.y), c, mob.speed/2)
                    item.speed_y = -w/80
                    if mob.speed < 0:
                        item.speed_x = -w/40
                    else:
                        item.speed_x = w/40
                        
                    item.tick = 300
                    mobs.append(item)
                    
            elif mob.mob == "zh":
                mob.move(mob.speed)
                mob.tick += 1
                if mob.tick%15==0:
                    mob.change(z)
            elif mob.mob == "ch":
                mob.move(mob.speed)
                mob.tick += 1
                if mob.tick%15==0:
                    mob.change(c)
            elif mob.mob == "zch":
                mob.move(mob.speed)
                mob.tick += 1
                if mob.tick%15==0:
                    mob.change(zc)
                    
                    
            elif mob.mob == "sp":
                mob.tick += 1
                mob.move(mob.speed)
                if mob.tick%30 == 0:
                    spider_step.play()
                    
            elif mob.mob == "sph":
                mob.move(mob.speed)
                mob.tick += 1
                if mob.tick%15 == 0:
                    mob.change(sp)
                
        for arrow in arrows:
            arrow.move()
            arrow.draw()
            if arrow.mask.overlap(land_mask, (-arrow.r.x, -arrow.r.y)):
                arrows.remove(arrow)
            for mob in mobs:
                if arrow.mask.overlap(mob.mask, (mob.r.x - arrow.r.x, mob.r.y - arrow.r.y)):
                    mob.hp -= 1
                    score += 1
                    # To not go further in the air
                    if mob.mask.overlap(land_mask, (-mob.r.x, -mob.r.y)):
                        mob.speed_y = -w/53.33
                        
                    mob.speed_x = steve.speed * 6 #w/133.33
                    
                    if mob.mob == "z":
                        mob.change(zh)
                        if mob.hp > 0:
                            if random.randint(0,1) == 0:
                                zombie_hurt1.play()
                            else:
                                zombie_hurt2.play()
                            
                    elif mob.mob == "c" or mob.mob == "cf":
                        mob.change(ch)
                        if mob.hp > 0:
                            creeper_hurt.play()
                            
                    elif mob.mob == "zc":
                        mob.change(zch)
                        if mob.hp > 0:
                            if random.randint(0,1) == 0:
                                zombie_hurt1.play()
                            else:
                                zombie_hurt2.play()
                    
                    
                    elif mob.mob == "sp":
                        mob.change(sph)
                        if mob.hp > 0:
                            spider_hurt.play()
                    
                    if mob.hp <= 0:
                        mobs.remove(mob)
                        # Score
                        score += 5
                        # Sound
                        if mob.mob == "zh":
                            zombie_death.play()
                        elif mob.mob == "ch":
                            creeper_death.play()
                        elif mob.mob == "zch":
                            zombie_death.play()
                            # Give the creeper back
                            mobs.append(Mob((mob.r.x, mob.r.y), c, mob.speed/abs(mob.speed)*w/800))
                            
                        elif mob.mob == "sph":
                            spider_death.play()

                    if arrow in arrows: # If arrows contains arrow
                        arrows.remove(arrow)
        # Steve        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steve.speed_x = -w/160
            steve.speed = -w/800
            steve.change(st)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steve.speed_x = w/160
            steve.speed = w/800
            steve.change(st)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if steve.mask.overlap(land_mask, (-steve.r.x, -steve.r.y)):
                steve.speed_y = -w/(800/22) # 22
                
        steve.tick += 1
        if steve.mob == "sth" and steve.tick%15==0:
            steve.change(st)
    
        steve.change_amount()
        # Collision of player
        for mob in mobs:
            if steve.mask.overlap(mob.mask, (mob.r.x - steve.r.x, mob.r.y - steve.r.y)) and not steve.mob == "sth" and steve.hittick > 30:
                if mob.mob == "z":
                    steve.hp -= 1
                elif mob.mob == "boom":
                    steve.hp -= 4
                elif mob.mob == "sp":
                    steve.hp -= 1
                    
                elif mob.mob == "c" and mob.tick < 300:
                    mob.tick = 300
                if mob.mob == "z" or mob.mob == "boom" or mob.mob == "sp":
                    steve.change(sth)
                    steve.hittick = 0
                    player_hurt.play()
                if steve.hp < 1:
                    alive = False
                if mob.mob == "z" or mob.mob == "boom" or mob.mob == "sp":
                    if steve.mask.overlap(land_mask, (-steve.r.x, -steve.r.y)):
                        steve.speed_y = -w/53.33 # -15
                
                    steve.speed_x = mob.speed/abs(mob.speed) * w/133.33 #6
                    
        # Boundaries
        if steve.r.x < 0:
            steve.r.x = 0
        elif steve.r.x > (-157*w/1200)+w:
            steve.r.x = (-157*w/1200)+w
        steve.draw()
        
        
        #0.9*w, -w/80

        #Other
        screen.blit(heart, (w/10, w/40))
        
        hp_font = pygame.font.SysFont("Snap ITC", round(w/16))
        hp_text = hp_font.render(str(steve.hp), True, (255,255,255))
        hp_rect = hp_text.get_rect(topleft=(w/35, w/57))
        screen.blit(hp_text, hp_rect)
        
        sc_font = pygame.font.SysFont("Snap ITC", round(w/16))
        sc_text = sc_font.render(str(score), True, (255,255,255))
        sc_rect = sc_text.get_rect(center=(w/2, h/10))
        screen.blit(sc_text, sc_rect)
        
        # Level display
        if (level_tick > 60 and level_tick) < 120 or (level == 1 and level_tick < 60):
            l_font = pygame.font.SysFont("Snap ITC", round(w/16))
            l_text = l_font.render("Level " + str(level), True, (255,255,255))
            l_rect = l_text.get_rect(center=(w/2, h/2))
            screen.blit(l_text, l_rect)
            
        game_tick += 1
        level_tick += 1
        
        steve.hittick += 1
        steve.shottick += 1
        
        if fps < 30:
            fps += 5
            
        pygame.display.flip()
        clock.tick(fps)


        
    if running:
        over = True
        
        
    # Died
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                alive = False
                over = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                over = False
        screen.fill((70,0,0))
            
        d_font = pygame.font.SysFont("Snap ITC", round(w/16))
        d_text = d_font.render("You Died!", True, (255,255,255))
        d_rect = d_text.get_rect(center=(w/2, h/3))
        screen.blit(d_text, d_rect)
        
        sc_font = pygame.font.SysFont("Snap ITC", round(w/25))
        sc_text = sc_font.render("Level: " + str(level) + " Score: "+ str(score), True, (255,255,255))
        sc_rect = sc_text.get_rect(center=(w/2, h/2))
        screen.blit(sc_text, sc_rect)
        
        pygame.display.flip()
        
pygame.quit()
