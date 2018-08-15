import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 155)

display_width = 800
display_height = 600

gameDispaly = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Serpent')

icon = pygame.image.load('appleicon.png')
pygame.display.set_icon(icon)
snakeHead = pygame.image.load('snakehead.png')
apple = pygame.image.load('apple.png')

clock = pygame.time.Clock()

block_size = 10
FPS = 20

direction = 'right'

smFont = pygame.font.SysFont('comicsansms', 25)
medFont = pygame.font.SysFont('comicsansms', 50)
lgFont = pygame.font.SysFont('comicsansms', 80)

def game_intro():
  intro = True
  while intro:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_c:
          intro = False
        if event.key == pygame.K_q:
          pygame.quit()
          quit()

    gameDispaly.fill(white)
    message_to_screen('Wlecome to Serpent', green, -150, 'large')
    message_to_screen('The objective of the game is ti eat as many apples as possible!', black, -30, 'small')
    message_to_screen('The more apples you eat, the longer you get', black, 10, 'small')
    message_to_screen('But, be careful... If you run into yourself, or the walls, you will DIE!', black, 50, 'small')

    message_to_screen('press "C" to play or "Q" to quit.', black, 180, 'small')

    pygame.display.update()
    clock.tick(5)

def snake(block_size, snakeList):
  if direction == 'right':
    head = pygame.transform.rotate(snakeHead, 270)
  if direction == 'left':
    head = pygame.transform.rotate(snakeHead, 90)
  if direction == 'up':
    head = snakeHead
  if direction == 'down':
    head = pygame.transform.rotate(snakeHead, 180)

  gameDispaly.blit(head,(snakeList[-1] [0], snakeList[-1][1]))

  for XnY in snakeList[:-1]:
    pygame.draw.rect(gameDispaly, blue, [XnY[0], XnY[1], block_size, block_size])

def text_objs(text, color, size):
  if size == 'small':
    textSurface = smFont.render(text, True, color)
  elif size == 'medium':
    textSurface = medFont.render(text, True, color)
  elif size == 'large':
    textSurface = lgFont.render(text, True, color)

  return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size='small'):
  textSurf, textRect = text_objs(msg, color, size)
  textRect.center = (display_width/2), (display_height/2) + y_displace
  gameDispaly.blit(textSurf, textRect)



def gameLoop():
  global direction
  direction = 'right'
  gameExit = False
  gameOver = False

  lead_x = display_width/2
  lead_y = display_height/2

  lead_x_change = 10
  lead_y_change = 0

  snakeList = []
  snakeLength = 1

  randAppleX = round(random.randrange(0, display_width - block_size)/10.0)*10.0
  randAppleY = round(random.randrange(0, display_height - block_size)/10.0)*10.0

  while not gameExit:

    while gameOver:
      gameDispaly.fill(white)
      message_to_screen('Game over!', red, -50, 'large')
      message_to_screen('press "C" to continue or "Q" to quit.', black, 50, 'small')
      pygame.display.update()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          gameOver = False
          gameExit = True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
            gameExit = True
            gameOver = False
          if event.key == pygame.K_c:
            gameLoop()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        gameExit = True
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          direction = 'left'
          lead_x_change = -block_size
          lead_y_change = 0
        elif event.key == pygame.K_RIGHT:
          direction = 'right'
          lead_x_change = block_size
          lead_y_change = 0
        elif event.key == pygame.K_UP:
          direction = 'up'
          lead_y_change = -block_size
          lead_x_change = 0
        elif event.key == pygame.K_DOWN:
          direction = 'down'
          lead_y_change = block_size
          lead_x_change = 0
 
    if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
      gameOver = True

    lead_x += lead_x_change  
    lead_y += lead_y_change    
    
    gameDispaly.fill(white)
    gameDispaly.blit(apple,(randAppleX, randAppleY))
    # pygame.draw.rect(gameDispaly, red, [randAppleX, randAppleY, block_size, block_size])    
    
    snakeHead = []
    snakeHead.append(lead_x)
    snakeHead.append(lead_y)
    snakeList.append(snakeHead)

    if len(snakeList) > snakeLength:
      del snakeList[0]

    for eachSegment in snakeList[:-1]:
      if eachSegment == snakeHead:
        gameOver= True

    snake(block_size, snakeList)
    
    pygame.display.update()
    
    if lead_x == randAppleX and lead_y == randAppleY:
      randAppleX = round(random.randrange(0, display_width - block_size)/10.0)*10.0
      randAppleY = round(random.randrange(0, display_height - block_size)/10.0)*10.0
      snakeLength += 1
    
    clock.tick(FPS)

  pygame.quit()
  quit()

game_intro()
gameLoop()