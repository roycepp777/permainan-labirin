from pygame import *

#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Calling the class constructor (Sprite):
        sprite.Sprite.__init__(self)
        # each sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        # each sprite must store the rect property - the rectangle which it's inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # the method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#class of the main player
class Player(GameSprite):
 #the method in which the sprite is controlled by the arrow keys of the keyboard
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Calling the class constructor (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        # horizontal movement first
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
            
        # if we go behind the wall, we'll stand right up to it
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # we're going to the right, the character's right edge appears right up to the left edge of the wall
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # if several walls were touched at once, then the right edge is the minimum possible
        elif self.x_speed < 0: # we're going to the left, then put the character's left edge right up to the right edge of the wall
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # if several walls have been touched, then the left edge is the maximum
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # if we go behind the wall, we'll stand right up to it
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # going down
            for p in platforms_touched:
                self.y_speed = 0
                # We're checking which of the platforms is the highest from the ones below, aligning with it, and then take it as our support:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # going up
            for p in platforms_touched:
                self.y_speed = 0 # the vertical speed is dampened when colliding with the wall
                self.rect.top = max(self.rect.top, p.rect.bottom) # aligning the upper edge along the lower edges of the walls that were touched
    # the "shot" method (we use the player's place to create a bullet there)
    def fire(self):
        bullet = Bullet('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

# the enemy sprite class   
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.initial_x = player_x  # Simpan posisi awal
        self.initial_y = player_y
        self.state = "patrol"  # Status awal: patrol
        self.side = "left"  # Gerakan horizontal awal

    def update(self):
        # Hitung jarak ke hero
        dx_to_hero = packman.rect.x - self.rect.x
        dy_to_hero = packman.rect.y - self.rect.y
        distance_to_hero = (dx_to_hero ** 2 + dy_to_hero ** 2) ** 0.5

        if distance_to_hero <= 100:  # Jika dalam radius, ubah status menjadi chasing
            self.state = "chasing"
        elif self.state == "chasing" and distance_to_hero > 100:  # Keluar radius, ubah ke returning
            self.state = "returning"

        if self.state == "chasing":  # Mengejar hero
            if distance_to_hero != 0:
                self.rect.x += self.speed * (dx_to_hero / distance_to_hero)
                self.rect.y += self.speed * (dy_to_hero / distance_to_hero)
                # new_x = self.rect.x + self.speed * (dx_to_hero / distance_to_hero)
                # new_y = self.rect.y + self.speed * (dy_to_hero / distance_to_hero)
                # self.rect.x = new_x
                # if sprite.spritecollide(self, barriers, False):
                #     self.kill()  # Hapus peluru jika menabrak dinding

                # # Cek tabrakan pada sumbu Y
                # self.rect.y = new_y
                # if sprite.spritecollide(self, barriers, False):
                #     self.kill()
        elif self.state == "returning":  # Kembali ke posisi awal
            dx_to_start = self.initial_x - self.rect.x
            dy_to_start = self.initial_y - self.rect.y
            distance_to_start = (dx_to_start ** 2 + dy_to_start ** 2) ** 0.5

            if distance_to_start > 1:
                self.rect.x += self.speed * (dx_to_start / distance_to_start)
                self.rect.y += self.speed * (dy_to_start / distance_to_start)
            else:
                self.state = "patrol"  # Setelah kembali ke posisi awal, ubah ke patrol
        elif self.state == "patrol":  # Gerakan horizontal
            if self.side == "left":
                self.rect.x -= self.speed
                if self.rect.x <= 540:  # Batas kiri
                    self.side = "right"
            else:
                self.rect.x += self.speed
                if self.rect.x >= win_width - 85:  # Batas kanan
                    self.side = "left"


# the bullet sprite's class  
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Calling the class constructor (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    # movement of a bullet
    def update(self):
        if monsters:
            # Find the nearest monster
            nearest_monster = min(monsters, key=lambda m: (m.rect.x - self.rect.x) ** 2 + (m.rect.y - self.rect.y) ** 2)
            dx = nearest_monster.rect.x - self.rect.x
            dy = nearest_monster.rect.y - self.rect.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance != 0:
                # Hitung perubahan posisi
                new_x = self.rect.x + self.speed * (dx / distance)
                new_y = self.rect.y + self.speed * (dy / distance)

                # Cek tabrakan pada sumbu X
                self.rect.x = new_x
                if sprite.spritecollide(self, barriers, False):
                    self.kill()  # Hapus peluru jika menabrak dinding

                # Cek tabrakan pada sumbu Y
                self.rect.y = new_y
                if sprite.spritecollide(self, barriers, False):
                    self.kill()  # Hapus peluru jika menabrak dinding

#Creating a window
win_width = 1000
win_height = 700
display.set_caption("Maze Game")
window = display.set_mode((win_width, win_height))
back = (120, 200, 100)#setting the color according to the RGB color scheme

#creating a group for the walls
barriers = sprite.Group()

#creating a group for the bullets
bullets = sprite.Group()

#creating a group for the monsters
monsters = sprite.Group()

#creating wall pictures
# w1 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro/Modul 6/aksesori_game/platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
# w2 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro/Modul 6/aksesori_game/platform2_v.png', 370, 100, 50, 400)
w3 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2_v.png', 500, 300, 50, 400)
w4 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2_v.png', 500, 100, 50, 200)
w5 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2.png', 0, 550, 400, 50)
w6 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2.png', 100, 400, 400, 50)
w7 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2.png', 0, 250, 400, 50)
w8 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2.png', 100, 100, 400, 50)
w9 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2_v.png', 650, 0, 50, 90)
w10 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2_v.png', 800, 0, 50, 90)
w11 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2_v.png', 950, 0, 50, 90)
w12 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2_v.png', 0, 0, 50, 50)
w13 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2_v.png', 870, 600, 50, 100)
w14 = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/platform2_v.png', 700, 600, 50, 100)

#adding walls to the group
# barriers.add(w1)
# barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)
barriers.add(w11)
# barriers.add(w12)
barriers.add(w13)
barriers.add(w14)

#creating sprites
packman = Player('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/hero.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/pac-1.png', win_width - 85, win_height - 100, 80, 80)

monster1 = Enemy('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/cyborg.png', win_width - 80, 100, 80, 80, 10)
monster2 = Enemy('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/cyborg.png', win_width - 80, 180, 80, 80, 15)
monster3 = Enemy('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/cyborg.png', win_width - 70, 260, 80, 80, 17)
monster4 = Enemy('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/cyborg.png', win_width - 70, 340, 80, 80, 19)
monster5 = Enemy('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/cyborg.png', win_width - 70, 420, 80, 80, 20)
monster6 = Enemy('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/cyborg.png', win_width - 70, 500, 80, 80, 30 )

#adding a monster to the group
monsters.add(monster1)
monsters.add(monster2)
# monsters.add(monster3)
# monsters.add(monster4)
# monsters.add(monster5)
# monsters.add(monster6)

#the variable responsible for how the game has ended
finish = False
#game loop
run = True
while run:
 #the loop is triggered every 0.05 seconds
    time.delay(50)
    #iterating through all the events that could have happened
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -10
            elif e.key == K_RIGHT:
                packman.x_speed = 10
            elif e.key == K_UP:
                packman.y_speed = -10
            elif e.key == K_DOWN:
                packman.y_speed = 10   
            elif e.key == K_SPACE:
                packman.fire()


        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0


#checking that the game is not finished yet
    if not finish:
        #updating the background every iteration
        window.fill(back)# fill the window with color
        
        #launching sprite movements
        packman.update()
        bullets.update()

        #updating them in a new location at each iteration of the loop
        packman.reset()
        #drawing the walls 2
        #w1.reset()
        #w2.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()


        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)


        #Checking the character's collision with the enemy and walls
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            #calculate the ratio
            img = image.load('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))


        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('D:/Data Scientist/Algoritmics/Python Pro I/Modul 6/File Eksekusi/aksesori_game/thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()
# display.update()

