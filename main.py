import pygame
import random

pygame.init()

#задаём переменные
WIDTH = 600
HEIGHT = 400
FPS = 30
BLACK = (0,0,0)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
running = True

#загружаем картинки
spaceshipImg = pygame.image.load('spaceship.png')
enemy0 = pygame.image.load('enemy0.png')
enemy1 = pygame.image.load('enemy1.png')
enemy2 = pygame.image.load('enemy2.png')
explosion0 = pygame.image.load('sprite_0.png')
explosion1 = pygame.image.load('sprite_1.png')
explosion2 = pygame.image.load('sprite_2.png')
explosion3 = pygame.image.load('sprite_3.png')
explosion4 = pygame.image.load('sprite_4.png') 
explosions = [explosion0,explosion1,explosion2,explosion3,explosion4]
hpImg = pygame.image.load('hp.png') 

spaceX = 280
spaceY = 300
spacedX = 0
hp = 3
hpImages = []

#появление иконок хп с помощью ф-ии
def refreshHP(hp,hpImages):
  x = WIDTH - 20
  for i in range(hp):
    hpImages.append([x,5])
    x -= 20

refreshHP(hp,hpImages)
bullets = []
enemyBullets = []
bullFrame = 5

#стрельба
def stepBullet(bullets,enemyBullets):
  for i in bullets:
    i[1] -= 5
    if i[1] < 0:
      bullets.remove(i)
  for i in enemyBullets:
    i[1] += 5
    if i[1] > HEIGHT:
      enemyBullets.remove(i) 

enX = 80
enY = 40
shape = 0
enemies = []

#задаём координаты рядов врага
for i in range(1,45):
  enemies.append([enX+40*((i-1)%11), enY, shape])
  if i % 11 == 0:
    enY += 45
    shape += 1 

def moveEnemies(enemies):
  for i in enemies:
    i[1] += 0.1

#проверка попадания во врага
def hit(bullets,enemies):
  for i in bullets:
    for enemie in enemies:
      bullet_x = i[0] 
      bullet_y = i[1]
      enemie_x = enemie[0]
      enemie_y = enemie[1]
      if enemie[2] == 100:
        continue
      if enemie_y <= bullet_y <= enemie_y+35 and enemie_x - 5 <= bullet_x <= enemie_x+35:
        enemies.append([enemie_x,enemie_y,100,0])
        enemies.remove(enemie)
        bullets.remove(i)  


#проверка попадания в игрока
def hitSpaceship(spaceX,spaceY,enemyBullets):
  for bullet in enemyBullets:
    bullet_x = bullet[0]
    bullet_y = bullet[1]
    if spaceY+5 <= bullet_y <= spaceY+55 and spaceX - 5 <= bullet_x <= spaceX+35: 
      enemyBullets.remove(bullet)
      return -1
  return 0   

def createBullet(enemies):
  x = random.randint(1,50)
  if x == 1:
    random.shuffle(enemies)
    if len(enemies) > 0:
      return [enemies[0][0]+18,enemies[0][1]+14]
  return 0

def getEnemyY(enemies):
  maxY = 0
  for i in enemies:
    if maxY < i[1]:
      maxY = i[1]
  return maxY + 40    

currentFrame = 0
#игровой цикл
while running:
  clock.tick(FPS)
  currentFrame += 1
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      pygame.quit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        spacedX = -5
      elif event.key == pygame.K_RIGHT:
          spacedX = 5
    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        spacedX = 0
      elif event.key == pygame.K_RIGHT:
        spacedX = 0

  screen.fill(BLACK)
  screen.blit(spaceshipImg,(spaceX,spaceY))
	
  if bullFrame > 0 and currentFrame % 5 == 0:
    bullets.append([spaceX+19,spaceY])
		
  if (5 <= spaceX and spacedX < 0) or (555 >= spaceX and spacedX > 0):
    spaceX += spacedX

  for i in bullets:
    pygame.draw.rect(screen,(255,255,255),(i[0],i[1],2,6))

  bull = createBullet(enemies)
  if bull != 0:
    enemyBullets.append(bull)  
  stepBullet(bullets,enemyBullets)
  
  #отрисовка пуль врагов
  for bullet in enemyBullets:
    pygame.draw.rect(screen,(255,0,0),(bullet[0],bullet[1],4,12))

  hp += hitSpaceship(spaceX,spaceY,enemyBullets)
  hpImages = []
  refreshHP(hp,hpImages)
  if hp <= 0:
    running = False

  for enemy in enemies:
    if enemy[2] == 0:
      screen.blit(enemy0,(enemy[0],enemy[1]))
    elif enemy[2] == 1:
      screen.blit(enemy1,(enemy[0],enemy[1]))
    elif enemy[2] == 2:
      screen.blit(enemy2,(enemy[0],enemy[1]))
    elif enemy[2] == 100:
      if enemy[3] > 4:
        enemies.remove(enemy) 
        continue 
      screen.blit(explosions[enemy[3]],(enemy[0],enemy[1]))
      enemy[3] += 1    
    else:
      screen.blit(enemy0,(enemy[0],enemy[1]))

  for i in hpImages:
    screen.blit(hpImg,(i[0],i[1]))  

  moveEnemies(enemies)
  hit(bullets,enemies)

  if getEnemyY(enemies) >= spaceY:
    running = False

  pygame.display.update()