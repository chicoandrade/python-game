# Snake Game!
import pygame
import sys
import random
import time

check_errors = pygame.init()

if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized!")

# Play Surface
screen_widht = 720
screen_height = 460
screen = pygame.display.set_mode((screen_widht, screen_height))  # display size on a tuple
pygame.display.set_caption("Snakes on a case!")

# Colours
color_black = pygame.Color(0, 0, 0)  # pygame.Color(r, g, b)
color_blue = pygame.Color(0, 0, 255)
color_green = pygame.Color(0, 255, 0)
color_red = pygame.Color(255, 0, 0)
color_white = pygame.Color(255, 255, 255)
color_brown = pygame.Color(164, 42, 42)

# Frames per second controller
fps_controller = pygame.time.Clock()

# More variables
framerate = 15
block_size = 20
snake_initial_x_position = block_size * 3
snake_initial_y_position = block_size
snake_position = [snake_initial_x_position, snake_initial_y_position]  # [x=horizontal, y=vertical] position
snake_body = [[snake_initial_x_position, snake_initial_y_position], [snake_initial_x_position - block_size, snake_initial_y_position], [snake_initial_x_position - block_size * 2, snake_initial_y_position]]  # snake body [x, y]*3 position
direction = 'RIGHT'
change_to = direction
pause = False
score = 0
msg_display = False
msg_time = time.time()
msg_duration = 2
apple_image = pygame.image.load("apple-icon.png").convert()
apple_image = pygame.transform.scale(apple_image, (int(block_size/2), int(block_size/2)))

def show_text(text="Nice try", color=color_blue, position=(int(screen_widht/2), 20)):
    text_font = pygame.font.SysFont("monaco", 72)  # pygame.font.SysFont(name, size)
    text_surface = text_font.render(text, True, color)  # gameover_font.render(text, antialias, color) - The surface where the font will be rendered
    text_rectangule = text_surface.get_rect()  # represents the rectangle of the surface
    text_rectangule.midtop = position  # (x=horizontal, y=vertical) coordinates
    screen.blit(text_surface, text_rectangule)  # puts the surface on the play surface


def quit_game():
    screen.fill(color_white)
    show_text(text="Bye", position=(int(screen_widht/2), int(screen_height/2)))
    pygame.display.flip()  # flips the frame to make the text appear
    time.sleep(1)
    pygame.quit()  # pygame exit
    sys.exit(0)  # console exit


# Game over function
def game_over():
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.load("gameover.mp3")
    pygame.mixer.music.play()
    show_score(0)
    show_text(text="Game Over!", color=color_red)
    pygame.display.flip()  # flips the frame to make the text appear
    time.sleep(3)
    quit_game()


def pop_food():
    position_x = (random.randrange(int(block_size/2), int(screen_widht/block_size))*block_size) - int(block_size/2)
    position_y = (random.randrange(int(block_size/2), int(screen_height/block_size))*block_size) - int(block_size/2)
    food_position = [position_x, position_y]
    return food_position, True


def show_score(choice=1):
    text_font = pygame.font.SysFont("monaco", 24)
    score_surface = text_font.render("Score: " + str(score), True, color_black)
    score_rectangle = score_surface.get_rect()
    if choice == 1:
        score_rectangle.midtop = (block_size*2, block_size*2)
    else:
        score_rectangle.midtop = (int(screen_widht/2), 100)
    screen.blit(score_surface, score_rectangle)  # puts the surface on the play surface


show_text(text="Starting Game", color=color_white)
pygame.display.flip()  # flips the frame to make the text appear
time.sleep(1)
food_position, food_spawn = pop_food()

pygame.mixer.music.load("pop1.mp3")

# Main logic of the game
while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Checks if user requested to quit
                quit_game()
            elif event.type == pygame.KEYDOWN:  # Checks if the user hit a key
                if pause == True:
                    time.sleep(1)
                if event.key == ord('p'):
                    if pause == False:
                        pause = True
                        show_text("PAUSED")
                    else:
                        pause = False
                if event.key == pygame.K_UP or event.key == ord('w'):  # Check if key hitted was the up arrow key or the w button
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Validation of direction
        if pause == False:
            if change_to == 'UP' and not direction == 'DOWN':
                direction = change_to
            if change_to == 'DOWN' and not direction == 'UP':
                direction = change_to
            if change_to == 'LEFT' and not direction == 'RIGHT':
                direction = change_to
            if change_to == 'RIGHT' and not direction == 'LEFT':
                direction = change_to

            if direction == 'UP':
                snake_position[1] = snake_position[1] - block_size  # [x = index(0) = horizontal, y = index(1) = vertical]
            if direction == 'DOWN':
                snake_position[1] = snake_position[1] + block_size
            if direction == 'LEFT':
                snake_position[0] = snake_position[0] - block_size
            if direction == 'RIGHT':
                snake_position[0] = snake_position[0] + block_size

            # Snake body mechanism
            snake_body.insert(0, list(snake_position))  # adds one piece in front of the body
            if snake_position[0] == food_position[0] - int(block_size/2) and snake_position[1] == food_position[1] - int(block_size/2):  # if the snake gets the food, we let the piece in front - she will grow
                score += 1
                framerate += 1
                pygame.mixer.music.play()
                food_spawn = False  # theres no more food
                food_position, food_spawn = pop_food()
                msg_display = True
                msg_time = time.time()
            else:
                snake_body.pop()  # snake didnt got the food, so we will remove the bottom piece, since we added one at the front

            screen.fill(color_white)
            # Drawings should be bellow this line, otherwise they will not appear

            for pos in snake_body:  # lets draw the snake body
                pygame.draw.rect(screen, color_green, pygame.Rect(pos[0], pos[1], block_size, block_size))  # pygame.draw.rect(play surface, object color, pygame.Rect(x-pos, y-pos, x-size, y-size))

            screen.blit(apple_image,(food_position),)
            #pygame.draw.circle(screen, color_brown, (food_position), int(block_size / 2))  # surface, color, position, radius, width

            if snake_position[0] > screen_widht or snake_position[0] < 0:  # if snakes goes outside the screen
                game_over()
            if snake_position[1] > screen_height or snake_position[1] < 0:
                game_over()

            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    game_over()

        if msg_display == True:
            now = time.time()
            if int(now - msg_time) < msg_duration:
                show_text(text="Nice!", position=(screen_widht/4, screen_height/4))
            else:
                msg_display = False

        show_score()
        pygame.display.flip() # update the frame
        fps_controller.tick(framerate) # controls the framerate
    except Exception as e:
        print(e)
        show_text(text="Error!")
        quit_game()
