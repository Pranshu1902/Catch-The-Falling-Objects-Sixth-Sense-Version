import pygame
import random
import cv2 as cv
import numpy as np


pygame.init()

red = [255,0,0]
green = (0, 255, 0)
blue = (0, 0, 128)
light_blue = [0,0,255]

score = 0

dis = pygame.display.set_mode((280,500))

# starting page
img = pygame.image.load('intro(2).png')

pygame.draw.rect(dis, red, [80,10,180,50])

dis.blit(img, (5,100))
font3 = pygame.font.Font('freesansbold.ttf', 40)

text3 = font3.render('Start', True, green, red)

textRect3 = text3.get_rect()  
textRect3.center = (170, 35)

dis.blit(text3, textRect3)
pygame.display.update()



dis.fill([255,255,255])

player = pygame.image.load('player.png') # 64 X 64 image

# player's coordinates
x = 100
y = 400

font = pygame.font.Font('freesansbold.ttf', 20)
value = font.render("Your Score: " + str(score), True, green, blue)
dis.blit(value, [330, 35])

# object coordinates

x_list = [30, 110, 190]

x_object = random.choice(x_list)

dis.blit(player, (x,y))

y_object_old = 10
y_object = 10

# background
bg = pygame.image.load('bg2.jpg')
dis.blit(bg, (0,0))

# sixth sense

cam = cv.VideoCapture(0)

lower_value = np.array([20,100,100])
upper_value = np.array([40,255,255])


run = True

def game(run, x,y,x_list, x_object, y_object, y_object_old, score, goal, delayer):
    while run:
        pygame.time.delay(100)
        dist = 80


        ret,frame = cam.read()
        frame = cv.flip(frame,1)
    
        w = frame.shape[1]
        h = frame.shape[0]
        
        image_smooth = cv.GaussianBlur(frame,(7,7),0)

        mask = np.zeros_like(frame)

        mask[50:350,30:350] = [255,255,255]

        image_roi = cv.bitwise_and(image_smooth,mask)
        cv.rectangle(frame,(50,150),(350,450),(0,0,255),2)
        cv.line(frame,(150,150),(150,450),(0,0,255),2)
        cv.line(frame,(250,150),(250,450),(0,0,255),2)


        image_hsv = cv.cvtColor(image_roi,cv.COLOR_BGR2HSV)
        image_threshold = cv.inRange(image_hsv,lower_value,upper_value)
    
        contours, hierachy = cv.findContours(image_threshold,\
                                             cv.RETR_TREE,\
                                             cv.CHAIN_APPROX_NONE)


        if(len(contours)!=0):
           areas = [cv.contourArea(c) for c in contours]
           max_index = np.argmax(areas)
           cnt = contours[max_index]

           M = cv.moments(cnt)
           if(M['m00']!=0):
               cx = int(M['m10']/M['m00'])
               cy = int(M['m01']/M['m00'])
               cv.circle(frame,(cx,cy),4,(0,0,255),-1)
  
               if cy in range(150,450):
                   if cx<150 :
                       x=20
                   elif cx>250:
                       x=180
                   else:
                        x = 100              

           cv.imshow('Frame',frame)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
    
        pygame.draw.rect(dis, red, (x_object, y_object_old, 50,50))
    
        if y_object_old < 440:
            y_object_old+=40
        elif y_object_old > 440:
            y_object_old = 10
            x_object = random.choice(x_list)
        
        dis.fill([255,255,255])
        dis.blit(bg, (0,0))
        pygame.draw.rect(dis, light_blue, (x_object, y_object_old, 50,50))
        value = font.render("Your score: "+str(score), True, green, red)
        goal_text = font.render("Goal: "+str(goal), True, green, red)

        font2 = pygame.font.Font('freesansbold.ttf', 40)
        lose_text = font2.render("You Lost", True, green, red)
        win_text = font2.render("You Won", True, green, red)
        dis.blit(goal_text, [10,10])
        dis.blit(value, [130, 35])#########
        dis.blit(player, (x,y))


    
        if y_object_old + 20 >= y:
        
            # catching
            if x_object >= x and x_object <= x+64:
                score+=1
            
            # missing
            else:
                dis.fill([255,255,255])
                dis.blit(player, (x,y))
                pygame.draw.rect(dis, light_blue, (x_object, y_object_old, 50, 50))
                value = font.render("Your Score: " + str(score), True, green, red)
                dis.blit(value, [130,35])
                dis.blit(lose_text, [50,200])
                pygame.display.update()
                pygame.time.delay(500)
                run = False

        # winning
        if goal == score:
            dis.fill([255,255,255])
            dis.blit(win_text, [50,200])
            pygame.display.update()
            pygame.time.delay(500)

    
    
        pygame.display.update()
        if delayer == 0:
            pygame.time.delay(500)
            delayer+=1

    cam.release()
    pygame.quit()


while True:
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x <= 280 and x >= 80 and y <= 60 and y >= 10:
                dis.fill([0,0,0])
                white = [255,255,255]

                font5 = pygame.font.Font('freesansbold.ttf', 30)
                value5 = font5.render("Choose your goal", True, green, blue)
                dis.blit(value5, [10, 60])

                pygame.draw.rect(dis, [0,255,0], [70,150,120,50])
                font_goal = pygame.font.Font('freesansbold.ttf', 20)
                value = font5.render("25", True, white, green)
                dis.blit(value, [110, 160])
                
                pygame.draw.rect(dis, [0,0,128], [70,230,120,50])
                value = font5.render("50", True, white, blue)
                dis.blit(value, [110, 240])
                
                pygame.draw.rect(dis, [255,0,0], [70,310,120,50])
                value = font5.render("75", True, white, red)
                dis.blit(value, [110, 320])
                
                pygame.display.update()

                while True:
                    x1, y1 = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if x1<=190 and x1>= 70 and y1<= 200 and y1>=150:
                                game(True, 100,400,[30,110,190],x_object,10,10,0, 25,0)
                            elif x1<=190 and x1>= 70 and y1<= 280 and y1>=230:
                                game(True, 100,400,[30,110,190],x_object,10,10,0, 50,0)
                            elif x1<=190 and x1>= 70 and y1<= 360 and y1>=310:
                                game(True, 100,400,[30,110,190],x_object,10,10,0, 75,0)
