import pygame; pygame.init()
import random; import math

#Display Screen Initialize
screen_width = 900; screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock() #clock is needed for internal time and setting speed, fps etc

#Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()

#Colors
white = (255, 255, 255); black = (0, 0, 0); red = (255, 0, 0)

#Score text rendering
font = pygame.font.SysFont(None, 30)
fontend = pygame.font.SysFont(None, 50)
def text_screen(txt, color, x, y):
    screen_text = font.render(txt, True, color)
    gameWindow.blit(screen_text, [x, y])
def end_text_screen(txt, color, x, y):
    screen_text = fontend.render(txt, True, color)
    gameWindow.blit(screen_text, [x, y])

#snake body
def snakebody(screen, color, snake_body, size):
    for x, y in snake_body:
        pygame.draw.rect(screen, color, [x, y, size, size])

#Food / Dot
def randomdot():
    x = random.randint(10, screen_width - 20)
    y = random.randint(10, screen_height - 20)
    return (x, y)

def home():
    exithome = False
    while not exithome:
        gameWindow.fill(white)
        end_text_screen("Welcome to Snake Game", black, 240 ,220)
        end_text_screen("Press Spacebar or Enter to Play", black, 190, 260)
        end_text_screen("Press Escape to Exit at Anytime", black, 190, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exithome = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    difficulty()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); quit()
        
        pygame.display.update()
        clock.tick(30)

def difficulty():
    exitscreen = False
    while not exitscreen:
        gameWindow.fill(white)
        end_text_screen("Press Space for normal difficulty", black, 180, 240)
        end_text_screen("Press 'H' for Hard difficulty", black, 220, 280)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exitscreen = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: gameloop()
                if event.key == pygame.K_h: hardgameloop()
                if event.key == pygame.K_BACKSPACE: home()
                if event.key == pygame.K_ESCAPE: pygame.quit(); quit()
        pygame.display.update()
        clock.tick(30)

#Game Loop
def gameloop():
    #Game specific vars
    exit_game = False; game_over = False
    fps = 30 #frames per second
    score = 0

    #Initial snake settings
    x_pos = 450; y_pos = 300; snake_length = 20 #lenght and width for one snake body block
    x_speed = 0; y_speed = 0
    snake_body = []; snake_body_length = 1
    curr_dir = "None"; paused = False

    d = randomdot(); x_dot = d[0]; y_dot = d[1]

    #high score:
    with open("hiscore_normal.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiscore_normal.txt", "w") as f:
                f.write(hiscore)
            gameWindow.fill(black)
            end_text_screen("GAME OVER!", red, 320, 200)
            end_text_screen("Press Enter to Play Again", red, 240, 250)
            end_text_screen("Press Escape to Quit", red, 270, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: home()
                    if event.key == pygame.K_ESCAPE: pygame.quit(); quit()
        else:
            if abs(x_pos - x_dot) < 20 and abs(y_pos - y_dot) < 20:
                d = randomdot(); x_dot = d[0]; y_dot = d[1]; score += 10
                snake_body_length += 1
                if score > int(hiscore):
                    hiscore = str(score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and curr_dir != "down": 
                        x_speed = 0; y_speed = -10; curr_dir = "up"
                    if event.key == pygame.K_DOWN and curr_dir != "up": 
                        x_speed = 0; y_speed = 10; curr_dir = "down"
                    if event.key == pygame.K_RIGHT and curr_dir != "left":
                        x_speed = 10; y_speed = 0; curr_dir = "right"
                    if event.key == pygame.K_LEFT and curr_dir != "right": 
                        x_speed = -10; y_speed = 0; curr_dir = "left"
                    if event.key == pygame.K_ESCAPE: pygame.quit(); quit()
                    if event.key == pygame.K_p: paused = not paused
                    if event.key == pygame.K_BACKSPACE: home()
            if not paused:
                x_pos += x_speed; y_pos += y_speed    
                if x_pos >= 900: x_pos = 0
                if x_pos < 0: x_pos = 900
                if y_pos >= 600: y_pos = 0
                if y_pos < 0: y_pos = 600
                
                head = []
                head.append(x_pos); head.append(y_pos)
                snake_body.append(head)

                if len(snake_body) > snake_body_length:
                    del snake_body[0]

                if head in snake_body[:-1]: game_over = True

            gameWindow.fill(black)
            if paused:
                end_text_screen("The game is paused", white, 300, 300)
            # pygame.draw.rect(gameWindow, white, [x_pos, y_pos, snake_length, snake_width])
            snakebody(gameWindow, white, snake_body, snake_length)
            pygame.draw.circle(gameWindow, red, (x_dot, y_dot), 10)
            text_screen("Score: " + str(score) + " "*2 + "Hiscore: " + hiscore, white, 5, 5)
        
        pygame.display.update() #is required whenver there is an update in the display such as filling color
        clock.tick(fps)

    pygame.quit()
    quit()

def hardgameloop():
    #Game specific vars
    exit_game = False; game_over = False
    fps = 60 #frames per second
    score = 0

    #Initial snake settings
    x_pos = 450; y_pos = 300; snake_length = 20 #lenght and width for one snake body block
    x_speed = 0; y_speed = 0
    snake_body = []; snake_body_length = 1
    curr_dir = "None"; paused = False

    d = randomdot(); x_dot = d[0]; y_dot = d[1]

    #high score:
    with open("hiscore_hard.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiscore_hard.txt", "w") as f:
                f.write(hiscore)
            gameWindow.fill(black)
            end_text_screen("GAME OVER!", red, 320, 200)
            end_text_screen("Press Enter to Play Again", red, 240, 250)
            end_text_screen("Press Escape to Quit", red, 270, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: home()
                    if event.key == pygame.K_ESCAPE: pygame.quit(); quit()
        else:
            if abs(x_pos - x_dot) < 20 and abs(y_pos - y_dot) < 20:
                d = randomdot(); x_dot = d[0]; y_dot = d[1]; score += 10
                snake_body_length += 1
                if score > int(hiscore):
                    hiscore = str(score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and curr_dir != "down": 
                        x_speed = 0; y_speed = -10; curr_dir = "up"
                    if event.key == pygame.K_DOWN and curr_dir != "up": 
                        x_speed = 0; y_speed = 10; curr_dir = "down"
                    if event.key == pygame.K_RIGHT and curr_dir != "left":
                        x_speed = 10; y_speed = 0; curr_dir = "right"
                    if event.key == pygame.K_LEFT and curr_dir != "right": 
                        x_speed = -10; y_speed = 0; curr_dir = "left"
                    if event.key == pygame.K_ESCAPE: pygame.quit(); quit()
                    if event.key == pygame.K_p: paused = not paused
                    if event.key == pygame.K_BACKSPACE: home()
            if not paused:
                x_pos += x_speed; y_pos += y_speed    
                # if x_pos >= 900: x_pos = 0
                # if x_pos < 0: x_pos = 900
                # if y_pos >= 600: y_pos = 0
                # if y_pos < 0: y_pos = 600
                if x_pos > 900 or x_pos < 0: game_over = True
                if y_pos > 600 or y_pos < 0: game_over = True
                
                head = []
                head.append(x_pos); head.append(y_pos)
                snake_body.append(head)

                if len(snake_body) > snake_body_length:
                    del snake_body[0]

                if head in snake_body[:-1]: game_over = True

            gameWindow.fill(black)
            if paused:
                end_text_screen("The game is paused", white, 300, 300)
            # pygame.draw.rect(gameWindow, white, [x_pos, y_pos, snake_length, snake_width])
            snakebody(gameWindow, white, snake_body, snake_length)
            pygame.draw.circle(gameWindow, red, (x_dot, y_dot), 10)
            text_screen("Score: " + str(score) + " "*2 + "Hiscore: " + hiscore, white, 5, 5)
        
        pygame.display.update() #is required whenver there is an update in the display such as filling color
        clock.tick(fps)

    pygame.quit()
    quit()

home()