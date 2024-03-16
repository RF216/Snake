# ************************************************************************
# Ryan Fu
# CSE Project D
# Blk 4
# June 17, 2021

# This program is my own work - RF
# Citations: Andrew Yeh helped with the dictionary funciton for opposite directions, and helping out with the logic for the coordinate system and snake eating logic (popping out last coordinate v.s. not popping it out)


import random
import pygame
pygame.font.init()

score = 0
high = 0
text = "" #Text for user input for eladerboard
score_font = pygame.font.SysFont("arial", 35)
leaderboard_font = pygame.font.SysFont("arial", 17)
menu_font = pygame.font.SysFont("arial", 60)

menu1 = menu_font.render("Ryan Fu - SNAKE", True, 'blue')
menu2 = menu_font.render("Press an arrow to continue.", True, 'blue')
menu3 = menu_font.render("To gain points, eat the food.", True, 'blue')
menu4 = menu_font.render("Don't run into walls or yourself", True, 'blue')
lose = score_font.render("You lost. Please enter your name for the scoreboard", True, 'blue')


class Window:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1001, 701))

        self.running = True #Sets main loop running

        self.grid = Grid(self.window) #Inherit from grid

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

    def mainLoop(self):
        while self.running: #While loop for the main function

            # render background
            self.window.fill((0, 140, 0))
            
            self.grid.showGrid() #Shows the grid
            
            self.grid.showSnake() #Shows the snake

            self.grid.showFood() #Shows the food
            
            for event in pygame.event.get(): #Defiens all the different user interactions (Key presses)
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.grid.snake.is_alive == False: #This is the leaderboard function, so only activates if snake is dead
                        global text
                        global score
                        if event.unicode.isalpha(): #Checks to make sure it is a letter
                            text += event.unicode #Displays empty text, adds letters based on what user types. 
                        if event.key == pygame.K_RETURN:#Press enter, text resets and added to the leaderboard
                            if score<10 and text != "": #Ensures correct formatting, if no text, doesn;t enter anything
                                with open("leaderboardsnake.txt","r") as file: #Opens file in read mode
                                    lines = file.readlines() #Reads all lines, and saves as a list
                                with open("leaderboardsnake.txt","w") as file: #Opens file in write mode
                                    file.write("".join(lines)) #Ensures proper spacing wiht one name and one point value every line cause spacing was not proper in text file
                                    file.write("") #Ensures proper spacing wiht one name and one point value every line
                                    file.write("\t".join([str(0)+str(score),text]))#Save point and name with a tab in between
                                    file.write("\n") #Ensures proper spacing occurs
                            elif score>=10 and text != "":
                                with open("leaderboardsnake.txt","r") as file: #Opens file in read mode
                                    lines = file.readlines() #Reads all lines, and saves as a list
                                with open("leaderboardsnake.txt","w") as file: #Opens file in write mode
                                    file.write("".join(lines)) #Ensures proper spacing wiht one name and one point value every line cause spacing was not proper in text file
                                    file.write("") #Ensures proper spacing wiht one name and one point value every line
                                    file.write("\t".join([str(score),text]))#Save point and name with a tab in between
                                    file.write("\n") #Ensures proper spacing occurs                                
                            text = ""
                            score = 0
                            self.grid.snake.is_alive = True #Makes the snake alive again but still, so user can't enter more inputs in the leaderboard
                        if event.key == pygame.K_BACKSPACE: #Backspace function
                            text = text[:-1]

                    if self.grid.snake.is_alive == True: #Snake only moves if it is alive
                        if event.key == pygame.K_LEFT:
                            self.grid.snake.changeDirection("LEFT")
                        if event.key == pygame.K_RIGHT:
                            self.grid.snake.changeDirection("RIGHT")
                        if event.key == pygame.K_DOWN:
                            self.grid.snake.changeDirection("DOWN")
                        if event.key == pygame.K_UP:
                            self.grid.snake.changeDirection("UP")                      
            
            if self.grid.snake.direction == "STILL" and self.grid.snake.is_alive == True: #At menu, snake is alive and still so this will draw menu. 
                self.window.blit(menu1, (260,180))
                self.window.blit(menu2, (170,280))
                self.window.blit(menu3, (165,330))
                self.window.blit(menu4, (130,380))
                      
            self.grid.moveSnake() #Funciton ot move the snake
     
            if self.grid.snake.is_alive == False: #If the snake dies, leaderboard will appear in function with previous enetring function
                self.window.blit(lose, (100,180))
                text_surface = score_font.render(text, True, 'blue')
                self.window.blit(text_surface, (100, 230))
                with open("leaderboardsnake.txt","r") as file: #Reads file and prints top 5 leaders
                    lines = file.readlines()
                    lines.sort(reverse=True) #Reverses so highest score appears first
                leaderboard1 = score_font.render(lines[0], True, 'blue')
                leaderboard2 = score_font.render(lines[1], True, 'blue')
                leaderboard3 = score_font.render(lines[2], True, 'blue')
                leaderboard4 = score_font.render(lines[3], True, 'blue')
                leaderboard5 = score_font.render(lines[4], True, 'blue')
                tryagain = leaderboard_font.render("Please type the name you want to appear and press enter. If you don;t want to be on hte leaderboard, press enter directly.", True, 'blue')
                self.window.blit(leaderboard1, (100,330)) 
                self.window.blit(leaderboard2, (100,380))
                self.window.blit(leaderboard3, (100,430))
                self.window.blit(leaderboard4, (100,480))
                self.window.blit(leaderboard5, (100,530))
                self.window.blit(leaderboard5, (100,530))
                self.window.blit(tryagain, (50, 630))             
                
            score_display = score_font.render("Your Score: " + str(score), True, 'blue') 
            high_score = score_font.render("High Score: " + str(high), True, 'blue')           
            self.window.blit(score_display, (0, 0)) #Continuously display the score        
            self.window.blit(high_score, (750, 0)) #Continuously display high score              

            pygame.display.update() #Updates. Under while loop, will continuously update
        
class Grid: #This is the basis of our coordinate grid
    def __init__(self, window):
        self.gridList = [[]] * 20 #Draw our grid. It's 20 by 20, but really 20 by 17, for ease of use

        self.window = window

        self.snake = Snake()

        self.food = Food()

        self.lastMovement = 0 #Ensures movement of snake, doesn't move too fast
        
    def showGrid(self):
            for i in range(21): #Draws the grid
                pygame.draw.line(self.window, (150,150,150), (i * 50, 0), (i * 50, 1000))
                pygame.draw.line(self.window, (150,150,150), (0, i * 50), (1000, i * 50))
                
    def showSnake(self):
        for i in self.snake.getCoordinatesOfSnake(): #shows the snake. Gets the coordinates and displays all of them
            rectangle = pygame.Rect(i[0] * 50 + 5, i[1] * 50 + 5, 41, 41)
            pygame.draw.rect(self.window, 'green', rectangle)

    def showFood(self):
        apple = pygame.image.load(r'apple.png')
        #rectangle = pygame.Rect(apple,(self.food.coord[0] * 50 + 5, self.food.coord[1] * 50 + 5), (41, 41)) #Shows food form food coordinates
        #pygame.draw.rect(self.window, 'red', rectangle)
        self.window.blit(pygame.transform.scale(apple, (41, 41)), (self.food.coord[0] * 50 + 5, self.food.coord[1] * 50 + 5))
        #screen.blit(pygame.transform.scale(pic, (500, 500)), (0, 0))

    def moveSnake(self):
        if self.snake.direction != "STILL":  
            if pygame.time.get_ticks() - self.lastMovement > 150: # Ensures movement of snake, doesn't move too fast. Only adds the coordinates after certain time elapses 
                self.lastMovement = pygame.time.get_ticks()
                ret = self.snake.addCoordinate(self.food.coord) #Add the coordinate
                if ret == 1: #Coordinate retunrs input based on collision. 1 is with food
                    self.food.newLocation()
                if ret == 2: #Collision with wall ro the snake itself
                    # code for when it crashes
                    global high 
                    global score
                    high = score
                    self.snake.is_alive = False
                    self.snake.reset() #Resets the position and length


class Snake:
    
    is_alive = True #Snake is alive
    
    def __init__(self):
        self.coord = [(3, 4), (4, 4), (5, 4)] #Initial coordinates
        self.direction = "STILL" #Initial direction

    def getCoordinatesOfSnake(self): #Returns the coordinates. Getter function
        return self.coord

    def addCoordinate(self, foodCoord):
        if self.direction == "STILL": #If still, just sits there
            self.coord = [(3, 4), (4, 4), (5, 4)]
        #Other directions add a block in fornt of snakee
        if self.direction == "RIGHT":
            self.coord.append((self.coord[-1][0] + 1, self.coord[-1][1]))
        if self.direction == "LEFT":
            self.coord.append((self.coord[-1][0] - 1, self.coord[-1][1]))
        if self.direction == "UP":
            self.coord.append((self.coord[-1][0], self.coord[-1][1] - 1))
        if self.direction == "DOWN":
            self.coord.append((self.coord[-1][0], self.coord[-1][1] + 1))
        if not foodCoord == self.coord[-1]: #If doesn't hit food, will pop the last block
            self.coord.pop(0)
            ret = 0
        else: #If hits food
            global score
            ret = 1
            score += 1
        if self.checkCollision(): #Checks collision
            ret = 2
        return ret

    def changeDirection(self, newDirection): #Change the direction based on arrow keys
        if self.direction != "STILL": #Sets opposite, makes it easier
            oppositeDict = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}
            if newDirection != self.direction and newDirection != oppositeDict[self.direction]:
                self.direction = newDirection
        if self.direction == "STILL": #If originally still, different things will happen
            self.direction = newDirection
            score = 0         
            self.is_alive = True

    def checkCollision(self): #Checks collision 
        for i in self.coord[:-1]: 
            if i == self.coord[-1]: #If hits a block aling the snake
                return True
        if not -1 < self.coord[-1][0] < 20: #If hits wall
            return True
        if not -1 < self.coord[-1][1] < 14:
            return True
        return False
    
    def reset(self): #Rests the snake
        self.coord = [(3, 4), (4, 4), (5, 4)]
        self.direction = "STILL"


class Food:
    def __init__(self): #Initial coordinates of food
        self.coord = (random.randint(0, 19), random.randint(0, 13))

    def newLocation(self): #New food location
        self.coord = (random.randint(0, 19), random.randint(0, 13))

mainWindow = Window() #Sets main Window as an object
mainWindow.mainLoop() #Declares the main loop
