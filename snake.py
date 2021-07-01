'''
Snake Game
This program implements a Snake Game using Pygame. Snake Game
is a game where the user plays as a snake and the goal of the game
is to have the highest score possible. Every three seconds a point is
added to the score and every time the player gets the snake to eat
a food block, three points is added to the score.
'''

import time
import random
import sys
import pygame

SIZE = 50
BACKGROUND_COLOR = 161, 195, 230

class Snake:
    ''' This class creates a Snake object '''
    def __init__(self, screen, length):
        self.screen = screen

        self.body = pygame.image.load('resources/block.jpg').convert()

        self.length = length
        self.x_position = [SIZE * 3] * length
        self.y_position = [SIZE * 3] * length

        self.direction = 'DOWN'

    def go_up(self):
        ''' This function makes the snake go up '''
        # print('moved up')
        self.direction = 'UP'

    def go_down(self):
        ''' This function makes the snake go down '''
        # print('moved down')
        self.direction = 'DOWN'

    def go_left(self):
        ''' This function makes the snake go left '''
        # print('moved left')
        self.direction = 'LEFT'

    def go_right(self):
        ''' This function makes the snake go right '''
        # print('moved right')
        self.direction = 'RIGHT'

    def draw(self):
        ''' This function draws the snake in the window '''
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, ((255, 255, 255)), (50, 50, 700, 700))
        for i in range(self.length):
            self.screen.blit(self.body, (self.x_position[i], self.y_position[i]))

    def slither(self):
        ''' This function controls the movement of the snake '''
        for i in range(self.length - 1, 0, -1):
            # move position to the position of the block in front of it
            # ex. x[2] moves to where x[1] was
            self.x_position[i] = self.x_position[i - 1]
            self.y_position[i] = self.y_position[i - 1]

        if self.direction == 'UP':
            # to move up change the head Y position to go up one size
            self.y_position[0] -= SIZE
        if self.direction == 'DOWN':
            self.y_position[0] += SIZE
        if self.direction == 'LEFT':
            self.x_position[0] -= SIZE
        if self.direction == 'RIGHT':
            self.x_position[0] += SIZE

        self.draw()

    def add_length(self):
        ''' This function adds length to the snake whenever it eats
        a food object '''
        self.length += 1
        self.x_position.append(-1)
        self.y_position.append(-1)

class Food:
    ''' This class creates a food object for the snake to eat '''
    def __init__(self, screen):
        self.screen = screen

        self.x_position = SIZE * random.randint(1, 14)
        self.y_position = SIZE * random.randint(1, 14)

        self.food = pygame.image.load('resources/food.jpg').convert()

    def draw(self):
        '''  This function draws the food object on the window '''
        self.screen.blit(self.food, (self.x_position, self.y_position))

    def new_food(self):
        ''' This function sets the location for a newly
        generated food object '''
        self.x_position = SIZE * random.randint(1, 14)
        self.y_position = SIZE * random.randint(1, 14)

class Window:
    ''' This class controls the Window and gameplay in the window '''
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('resources/background.wav')
        pygame.mixer.music.play(-1)
        (width, height) = (800, 800)
        self.screen = pygame.display.set_mode((width, height))
        self.snake = Snake(self.screen, 2)
        self.food = Food(self.screen)
        self.initial_time = time.time()
        self.start_time = time.time()
        self.time_point = 0
        self.score = 0

    def set_menu_window(self):
        ''' This functions sets the menu window for the startup menu '''
        running = True

        while running:
            self.check_event()
            self.menu()

    def set_game_window(self):
        ''' This function sets the game window for gameplay'''
        running = True
        self.screen.fill(BACKGROUND_COLOR)
        self.start_time = time.time()
        self.time_point = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_UP:
                        self.snake.go_up()
                    if event.key == pygame.K_DOWN:
                        self.snake.go_down()
                    if event.key == pygame.K_LEFT:
                        self.snake.go_left()
                    if event.key == pygame.K_RIGHT:
                        self.snake.go_right()
                elif event.type == pygame.QUIT:
                    running = False
            self.game()

            time.sleep(0.1)

    def menu(self):
        ''' This functions controls the startup menu '''
        self.screen.fill((169, 235, 169))
        text = pygame.font.SysFont('arial', 60, bold = True)
        title = text.render('SNAKE GAME', True, (214, 77, 77))
        self.screen.blit(title, (200, 220))
        text = pygame.font.SysFont('arial', 25)
        line2 = text.render('Maia Nguyen | CPSC-386-01 Summer \'21', True, (214, 77, 77))
        line3 = text.render('Use arrow keys to move up, down, left or right' , True, (84, 138, 86))
        line4 = text.render('Don\'t go out of the white area or you die!' , True, (84, 138, 86))
        line5 = text.render('Every 3 seconds you survive is +1 point' , True, (84, 138, 86))
        line6 = text.render('Every food eaten is +3 points' , True, (84, 138, 86))
        line7 = text.render('Press Enter to play. Press Escape to quit.', True, (214, 77, 77))
        self.screen.blit(line2, (185, 280))
        self.screen.blit(line3, (165, 320))
        self.screen.blit(line4, (200, 360))
        self.screen.blit(line5, (200, 400))
        self.screen.blit(line6, (255, 440))
        self.screen.blit(line7, (200, 480))
        pygame.display.flip()

    def game(self):
        ''' This function controls gameplay controls '''
        self.snake.slither()
        self.food.draw()
        self.show_score()
        pygame.display.flip()
        self.continue_game()

    def show_score(self):
        ''' This function displays the current score '''
        current_time = time.time() - self.start_time
        if (current_time % 3) <= 0.1:
            self.time_point +=  1
        self.score = self.time_point + ((self.snake.length * 3) - 7)
        text = pygame.font.SysFont('arial', 25)
        score = text.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score, (650, 10))

    def check_event(self):
        ''' This function checks what key is pressed '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.snake = Snake(self.screen, 2)
                self.set_game_window()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def continue_game(self):
        ''' This function tests if game can be continued '''
        # check if snake has hit the food
        if self.hits_something(self.food.x_position, self.food.y_position):
            sound = pygame.mixer.Sound('resources/crunch.wav')
            pygame.mixer.Sound.play(sound)
            self.snake.add_length()
            self.food.new_food()

        # check if snake hits itself
        for i in range(1, self.snake.length):
            if self.hits_something(self.snake.x_position[i], self.snake.y_position[i]):
                sound = pygame.mixer.Sound('resources/bonk.wav')
                pygame.mixer.Sound.play(sound)
                time.sleep(1)
                running = True
                while running is True:
                    self.game_over()
                    pygame.display.flip()
                    self.check_event()

        #check if snake hits border
        if (self.snake.x_position[0] > 749 or self.snake.x_position[0] < 50 or
            self.snake.y_position[0] > 749 or self.snake.y_position[0] < 50):
            sound = pygame.mixer.Sound('resources/bonk.wav')
            pygame.mixer.Sound.play(sound)
            time.sleep(1)
            running = True
            while running is True:
                self.game_over()
                pygame.display.flip()
                self.check_event()
        if self.snake.length >= 196:
            print('You won!')
            running = True
            while running:
                self.game_over()
                pygame.display.flip()
                self.check_event()
        return True

    def hits_something(self, other_x, other_y):
        ''' This functions checks if the snake head hits something '''
        if self.snake.x_position[0] >= other_x:
            if self.snake.x_position[0] < other_x + SIZE:
                if self.snake.y_position[0] >= other_y:
                    if self.snake.y_position[0] < other_y + SIZE:
                        return True
        return False

    def game_over(self):
        ''' This function controls the game over scene '''
        self.screen.fill((214, 77, 77))
        text = pygame.font.SysFont('arial', 20)
        died = text.render(f"You died! Score is {self.score}", True, (255, 255, 255))
        self.screen.blit(died, (200, 320))
        play_again = text.render("Press Enter to play again. Press Escape to quit.",
            True, (255, 255, 255))
        self.screen.blit(play_again, (200, 370))

def main():
    ''' main function that handles the running of the program '''
    window = Window()
    window.set_menu_window()

if __name__ == '__main__':
    main()
