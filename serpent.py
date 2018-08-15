import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 155)
gray = (195, 195, 195)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Serpent')

icon = pygame.image.load('appleicon.png')
pygame.display.set_icon(icon)
snakeHead = pygame.image.load('snakehead.png')
apple = pygame.image.load('apple.png')

clock = pygame.time.Clock()

block_size = 10
FPS = 20

# highScore = 0
direction = 'right'

smFont = pygame.font.SysFont('comicsansms', 25)
medFont = pygame.font.SysFont('comicsansms', 50)
lgFont = pygame.font.SysFont('comicsansms', 80)

def pause():
  paused = True
  message_to_screen('Paused', black, -100, 'large')
  message_to_screen('Press "Space-bar" to continue or "Esc" to quit.', black, 25, 'small')
  
  pygame.display.update()
  while paused:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          paused = False
        elif event.key == pygame.K_ESCAPE:
          pygame.quit()
          quit()

def score(score):
  text = smFont.render('Score: '+str(score), True, black)
  gameDisplay.blit(text, [0, 0])

# def highestScore(score):
#   text = smFont.render('High-Score: '+str(score), True, black)
#   gameDisplay.blit(text, [0, 30])
 
def randAppleGen():
  randAppleX = round(random.randrange(0, display_width - block_size)/10.0)*10.0
  randAppleY = round(random.randrange(0, display_height - block_size)/10.0)*10.0

  return randAppleX,randAppleY

def game_intro():
  intro = True
  while intro:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          intro = False
        elif event.key == pygame.K_ESCAPE:
          gameExit = True
          gameOver = False

    gameDisplay.fill(gray)
    message_to_screen('Welcome to Serpent', green, -150, 'large')
    message_to_screen('The objective of the game is to eat as many apples as possible!', black, -30, 'small')
    message_to_screen('The more apples you eat, the longer you get.', black, 10, 'small')
    message_to_screen('But, be careful... If you run into yourself, or the walls, you will die.', black, 50, 'small')
    message_to_screen('During game play, press "Space-bar" to pause.', black, 90, 'small')
    message_to_screen('Press "Space-bar" to continue or "Esc" to quit.', black, 180, 'small')

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

  gameDisplay.blit(head,(snakeList[-1] [0], snakeList[-1][1]))

  for XnY in snakeList[:-1]:
    pygame.draw.rect(gameDisplay, blue, [XnY[0], XnY[1], block_size, block_size])

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
  gameDisplay.blit(textSurf, textRect)

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

  randAppleX, randAppleY = randAppleGen()

  while not gameExit:

    while gameOver:
      gameDisplay.fill(gray)
      message_to_screen('Game over!', red, -50, 'large')
      message_to_screen('Press "Space-bar" to continue or "Esc" to quit.', black, 50, 'small')
      score(snakeLength - 1)
      pygame.display.update()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          gameOver = False
          gameExit = True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            gameExit = True
            gameOver = False
          if event.key == pygame.K_SPACE:
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
        elif event.key == pygame.K_SPACE:
          pause()
        elif event.key == pygame.K_ESCAPE:
          gameExit = True
          gameOver = False
 
    if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
      gameOver = True

    lead_x += lead_x_change  
    lead_y += lead_y_change    
    
    gameDisplay.fill(gray)
    gameDisplay.blit(apple,(randAppleX, randAppleY))
    
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
    score(snakeLength-1)

    # if snakeLength-1 >= highScore:
    #   highestScore(snakeLength-1)
    # highScore = snakeLength-1
    
    pygame.display.update()
    
    if lead_x == randAppleX and lead_y == randAppleY:
      randAppleX, randAppleY = randAppleGen()
      snakeLength += 1
    
    clock.tick(FPS)
  
  pygame.quit()
  quit()

game_intro()
gameLoop()