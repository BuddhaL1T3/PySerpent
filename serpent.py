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

img = pygame.image.load('snakehead.png')

clock = pygame.time.Clock()

block_size = 10
FPS = 30

font = pygame.font.SysFont(None, 25)

def snake(block_size, snakeList):
  for XnY in snakeList:
    pygame.draw.rect(gameDispaly, blue, [XnY[0], XnY[1], block_size, block_size])

def text_objs(text, color):
  textSurface = font.render(text, True, color)
  return textSurface, textSurface.get_rect()

def message_to_screen(msg, color):
  textSurf, textRect = text_objs(msg,color)
  # screen_text = font.render(msg, True, color)
  # gameDispaly.blit(screen_text, [display_width/2, display_height/2])
  textRect.center = (display_width/2), (display_height/2)
  gameDispaly.blit(textSurf, textRect)



def gameLoop():

  gameExit = False
  gameOver = False

  lead_x = display_width/2
  lead_y = display_height/2

  lead_x_change = 0
  lead_y_change = 0

  snakeList = []
  snakeLength = 1

  randAppleX = round(random.randrange(0, display_width - block_size)/10.0)*10.0
  randAppleY = round(random.randrange(0, display_height - block_size)/10.0)*10.0

  while not gameExit:

    while gameOver:
      gameDispaly.fill(white)
      message_to_screen('Game over, press "C" to continue or "Q" to quit.', red)
      pygame.display.update()

      for event in pygame.event.get():
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
          lead_x_change = -block_size
          lead_y_change = 0
        elif event.key == pygame.K_RIGHT:
          lead_x_change = block_size
          lead_y_change = 0
        elif event.key == pygame.K_UP:
          lead_y_change = -block_size
          lead_x_change = 0
        elif event.key == pygame.K_DOWN:
          lead_y_change = block_size
          lead_x_change = 0

      # if event.type == pygame.KEYUP:
      #   if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
      #     lead_x_change = 0
      #   if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
      #     lead_y_change = 0

      if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
        gameOver = True

    lead_x += lead_x_change  
    lead_y += lead_y_change    
    
    gameDispaly.fill(white)
    pygame.draw.rect(gameDispaly, red, [randAppleX, randAppleY, block_size, block_size])    
    
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

gameLoop()