import pygame
import random
import time

pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Лабиринт')

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)      # Красный игрок
yellow = (255, 255, 0) # Желтый игрок
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (50, 50, 50)

# Параметры стен и дверей
line_width = 10
line_gap = 40
line_offset = 20
door_width = 20
door_gap = 40
max_openings_per_line = 5

# Параметры игрока
player_radius = 10
player_speed = 5

# Параметры финиша
finish_x = 20
finish_y = line_offset
finish_radius = 15

# Флаг победы
game_won = False
winner = None  # Переменная для хранения победителя

# Таймер
game_time = 60  # Время игры в секундах
start_time = None

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Управление игроками
controls = {
    'player1': {
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT
    },
    'player2': {
        'up': [pygame.K_w, pygame.K_c],  # W или Ц
        'down': [pygame.K_s, pygame.K_k],  # S или К
        'left': [pygame.K_a, pygame.K_f],  # A или Ф
        'right': [pygame.K_d, pygame.K_y]  # D или Ы
    }
}

def reset_game():
    global player1_x, player1_y, player2_x, player2_y, game_won, lines, start_time, winner
    player1_x = screen_width - 12
    player1_y = screen_height - line_offset
    player2_x = screen_width - 12
    player2_y = screen_height - (line_offset + 30)  # Второй игрок ниже первого
    game_won = False
    winner = None
    
    global start_time
    start_time = time.time()
    
    lines = []
    for i in range(0, screen_width, line_gap):
        rect = pygame.Rect(i, 0, line_width, screen_height)
        num_openings = random.randint(1, max_openings_per_line)
        if num_openings == 1:
            door_pos = random.randint(line_offset + door_width, screen_height - line_offset - door_width)
            lines.append(pygame.Rect(i, 0, line_width, door_pos - door_width))
            lines.append(pygame.Rect(i, door_pos + door_width, line_width, screen_height - door_pos - door_width))
        else:
            opening_positions = [0] + sorted([random.randint(line_offset + door_width, screen_height - line_offset - door_width) for _ in range(num_openings - 1)]) + [screen_height]
            for j in range(num_openings):
                lines.append(pygame.Rect(i, opening_positions[j], line_width, opening_positions[j + 1] - opening_positions[j] - door_width))

reset_game()

def draw_modal_window():
    modal_width = 300
    modal_height = 150
    modal_x = (screen_width - modal_width) // 2
    modal_y = (screen_height - modal_height) // 2

    pygame.draw.rect(screen, gray, (modal_x, modal_y, modal_width, modal_height))
    pygame.draw.rect(screen, white, (modal_x, modal_y, modal_width, modal_height), 3)  # Рамка

    # Выводим текст победителя тем же цветом, что и игрок
    win_text = font.render(f"{winner} выиграл!", True, yellow if winner == "Второй игрок" else red)
    screen.blit(win_text, (modal_x + (modal_width - win_text.get_width()) // 2, modal_y + 30))

    instruction_text = font.render("Нажмите 'R' для перезапуска", True, white)
    screen.blit(instruction_text, (modal_x + (modal_width - instruction_text.get_width()) // 2, modal_y + 80))

# Функция для получения нажатой клавиши с учетом раскладки
def get_key_press(keys, key_list):
    return any(keys[k] for k in key_list)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset_game()

    if not game_won:
        # Управление первым игроком (стрелки)
        if keys[controls['player1']['left']] and player1_x > player_radius:
            player1_x -= player_speed
        elif keys[controls['player1']['right']] and player1_x < screen_width - player_radius:
            player1_x += player_speed
        elif keys[controls['player1']['up']] and player1_y > player_radius:
            player1_y -= player_speed
        elif keys[controls['player1']['down']] and player1_y < screen_height - player_radius:
            player1_y += player_speed

        # Управление вторым игроком (WASD и русские клавиши)
        if get_key_press(keys, controls['player2']['left']):
            player2_x -= player_speed
        if get_key_press(keys, controls['player2']['right']):
            player2_x += player_speed
        if get_key_press(keys, controls['player2']['up']):
            player2_y -= player_speed
        if get_key_press(keys, controls['player2']['down']):
            player2_y += player_speed

        # Проверка выхода второго игрока за границы экрана
        if player2_x < player_radius:
            player2_x = player_radius
        elif player2_x > screen_width - player_radius:
            player2_x = screen_width - player_radius
        if player2_y < player_radius:
            player2_y = player_radius
        elif player2_y > screen_height - player_radius:
            player2_y = screen_height - player_radius

        # Проверка столкновений игроков со стенами
        player1_rect = pygame.Rect(player1_x - player_radius, player1_y - player_radius, player_radius * 2, player_radius * 2)
        player2_rect = pygame.Rect(player2_x - player_radius, player2_y - player_radius, player_radius * 2, player_radius * 2)

        for line in lines:
            if line.colliderect(player1_rect):
                if player1_x > line.left and player1_x < line.right:
                    if player1_y < line.top:
                        player1_y = line.top - player_radius
                    else:
                        player1_y = line.bottom + player_radius
                elif player1_y > line.top and player1_y < line.bottom:
                    if player1_x < line.left:
                        player1_x = line.left - player_radius
                    else:
                        player1_x = line.right + player_radius

            if line.colliderect(player2_rect):
                if player2_x > line.left and player2_x < line.right:
                    if player2_y < line.top:
                        player2_y = line.top - player_radius
                    else:
                        player2_y = line.bottom + player_radius
                elif player2_y > line.top and player2_y < line.bottom:
                    if player2_x < line.left:
                        player2_x = line.left - player_radius
                    else:
                        player2_x = line.right + player_radius

        # Проверка достижения финиша
        if (player1_x - finish_x) ** 2 + (player1_y - finish_y) ** 2 <= (finish_radius + player_radius) ** 2:
            game_won = True
            winner = "Первый игрок"
        elif (player2_x - finish_x) ** 2 + (player2_y - finish_y) ** 2 <= (finish_radius + player_radius) ** 2:
            game_won = True
            winner = "Второй игрок"

    screen.fill(black)

    for line in lines:
        pygame.draw.rect(screen, green, line)

    pygame.draw.circle(screen, red, (player1_x, player1_y), player_radius)
    pygame.draw.circle(screen, yellow, (player2_x, player2_y), player_radius)

    pygame.draw.circle(screen, blue, (finish_x, finish_y), finish_radius)

    # Таймер
    elapsed_time = time.time() - start_time
    remaining_time = game_time - int(elapsed_time)

    timer_text = font.render(f"Осталось времени: {remaining_time}", True, white)
    screen.blit(timer_text, (50, 10))

    if remaining_time <= 0:
        game_won = True
        winner = "Никто"

    if game_won:
        draw_modal_window()

    pygame.display.update()
    clock.tick(60)
