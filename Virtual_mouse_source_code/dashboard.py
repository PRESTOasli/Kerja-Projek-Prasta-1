import pygame
import subprocess
import sys


 #create display windows
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT ))
pygame.display.set_caption('Virtual Mouse Aplication')

#load button image
on_img = pygame.image.load('on-button.png')
off_img = pygame.image.load('off-button.png')
log_out_img = pygame.image.load('log-out.png')

#button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale),int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False
    def draw(self):
        action = False

        #draw  button on screen

        #get mouse positions
        pos = pygame.mouse.get_pos()
        # print(pos)

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            # print('HOVER')
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


#create button instances
on_button = Button(200, 140, on_img, 0.65)
off_button = Button(430, 140, off_img, 0.65)
log_out_button = Button(670, 440, log_out_img, 0.20)

module_state = "OFF"
subprocess_instance = None

#game loop
run = True
while run:

    screen.fill((202, 228, 241))
    if on_button.draw() == True:
        print('ON')
        subprocess_instance = subprocess.Popen([sys.executable,"gtau-ah_capek.py"])
        module_state = "ON"
    if off_button.draw() == True:
        if module_state == "ON":
            print('OFF')
            subprocess_instance.terminate()
            module_state = "OFF"
    if log_out_button.draw() == True:
        print('log out')
        pygame.display.iconify()
        subprocess_instance = subprocess.Popen([sys.executable, "main.py"])
        pygame.quit()
        # subprocess_instance = subprocess.Popen([sys.executable,"gtau-ah_capek.py"])
        module_state = "ON"
    #even handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()