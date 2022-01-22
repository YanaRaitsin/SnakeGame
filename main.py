import pygame
from pygame.locals import *
import time
import random

BLOCK_SIZE = 40
BACKGROUND_COLOR = (0,0,0)
class RedDot:
    def __init__(self, parent_screen):
        self.redDotImage = pygame.image.load("resources/redot.jpg").convert()
        self.parent_screen = parent_screen
        self.x = BLOCK_SIZE*3
        self.y = BLOCK_SIZE*3
    
    def draw(self):
        self.parent_screen.blit(self.redDotImage,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*BLOCK_SIZE
        self.y = random.randint(1,19)*BLOCK_SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snakeBlock = pygame.image.load("resources/snakeblock.jpg").convert()
        self.length = 1
        self.x=[BLOCK_SIZE]
        self.y=[BLOCK_SIZE]
        self.direction = 'right'

    def increaseLength(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((BACKGROUND_COLOR))
        for i in range(self.length):
            self.parent_screen.blit(self.snakeBlock,(self.x[i],self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'
    
    def move(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= BLOCK_SIZE
        if self.direction == 'right':
            self.x[0] += BLOCK_SIZE
        if self.direction == 'up':
            self.y[0] -= BLOCK_SIZE
        if self.direction == 'down': 
            self.y[0] += BLOCK_SIZE
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Amazing Snake")
        pygame.mixer.init() #init sounds
        self.playBackdroung()
        self.windowWidth = 1000
        self.windowHeight = 800
        self.surface = pygame.display.set_mode((self.windowWidth,self.windowHeight))
        self.surface.fill((BACKGROUND_COLOR))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.redDot = RedDot(self.surface)
        self.redDot.draw()
        self.score = 0

    def isCollision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + BLOCK_SIZE:
            if y1 >= y2 and y1 < y2 + BLOCK_SIZE:
                return True
        return False

    def playBackdroung(self):
        pygame.mixer.music.load("resources/backgroundmusic.mp3")
        pygame.mixer.music.play()
    
    def isCollisionWithScreen(self,x1,x2,y1,y2):
        if x1 >= x2 or x1 <0 or y1 >= y2 or y1 <0:
            return True
        return False

    def play(self):
            #changing the direction of the snake
            self.snake.move()
            #draw the red dot
            self.redDot.draw()
            #increasing the score
            self.displayScore()
            pygame.display.flip()
            #hitting the red dot
            if self.isCollision(self.snake.x[0], self.snake.y[0], self.redDot.x, self.redDot.y):
                self.snake.increaseLength()
                self.redDot.move()
                self.score+=1
            if self.isCollisionWithScreen(self.snake.x[0], self.windowWidth, self.snake.y[0], self.windowHeight):
                raise "Game Over"
            #snake colliding with itself
            for i in range(3, self.snake.length):
                if self.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                    raise "Game Over" #exception
    
    def displayScore(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def gameOver(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your score is {self.score}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300)) #show the line in the middle of the screen
        line2 = font.render(f"To play again, press Eneter. To exit press Escape.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()
        self.score=0

    def resetGame(self):
        self.snake = Snake(self.surface)
        self.redDot = RedDot(self.surface)
        self.score=0

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.gameOver()
                pause = True
                self.resetGame()

            time.sleep(.15)

if __name__ == "__main__":
    game = Game()
    game.run()
