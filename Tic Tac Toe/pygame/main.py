# Tic Tac Toe

# Autor y fecha
# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 28 October, 2021

import random                # Importa el módulo random para seleccionar jugador inicial al azar
import pygame                # Importa la librería pygame para gráficos y eventos
from objects import Rect, generate_boxes, create_board  # Importa funciones y clases personalizadas
from logic import isBoardFull, check_win                # Importa funciones de lógica del juego

pygame.init()                # Inicializa todos los módulos de pygame
SCREEN = WIDTH, HEIGHT = (288, 512)  # Define el tamaño de la ventana

info = pygame.display.Info() # Obtiene información de la pantalla
width = info.current_w       # Ancho de la pantalla
height = info.current_h      # Alto de la pantalla

# Selecciona el modo de pantalla según la orientación
if width >= height:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)  # Ventana sin bordes
else:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)  # Pantalla completa

clock = pygame.time.Clock()  # Reloj para controlar FPS
FPS = 60                    # Frames por segundo

# COLORES *********************************************************************

WHITE = (225,225,225)        # Color blanco
BLACK = (0, 0, 0)            # Color negro
GRAY = (32, 33, 36)          # Gris oscuro
BLUE = (0, 90, 156)          # Azul
ORANGE = (208, 91, 3)        # Naranja

# IMÁGENES ********************************************************************

bg1 = pygame.image.load('c:/GitHub/Python-Games/Tic Tac Toe/pygame/Assets/bg1.png')  # Carga fondo 1
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT-10))                                # Escala fondo 1

bg2 = pygame.image.load('c:/GitHub\Python-Games/Tic Tac Toe/pygame/Assets/bg2.png')  # Carga fondo 2
bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT-10))                                # Escala fondo 2

replay_image = pygame.image.load('c:/GitHub/Python-Games/Tic Tac Toe/pygame/Assets/replay.png')  # Carga imagen de reinicio
replay_image = pygame.transform.scale(replay_image, (36, 36))                                   # Escala imagen de reinicio
replay_rect = replay_image.get_rect()                                                           # Obtiene el rectángulo de la imagen
replay_rect.x = WIDTH - 110                                                                     # Posición X del botón de reinicio
replay_rect.y = 210                                                                             # Posición Y del botón de reinicio

# FUNCIONES DEL TABLERO ************************************************************

board = create_board()           # Crea el tablero vacío
box_list = generate_boxes()      # Genera las casillas del tablero
players = ['X', 'O']             # Lista de jugadores
current_player = random.randint(0, 1)  # Selecciona jugador inicial al azar
text = players[current_player]         # Marca del jugador actual

# FUENTES **********************************************************************

scoreX = 0                      # Puntuación de X
scoreO = 0                      # Puntuación de O

font1 = pygame.font.Font('c:/GitHub/Python-Games/Tic Tac Toe/pygame/Fonts/PAPYRUS.TTF', 17)   # Fuente para marcador
font2 = pygame.font.Font('c:/GitHub/Python-Games/Tic Tac Toe/pygame/Fonts/CHILLER.TTF', 30)   # Fuente para título
font3 = pygame.font.Font('c:/GitHub/Python-Games/Tic Tac Toe/pygame/Fonts/CHILLER.TTF', 40)   # Fuente para resultado

tic_tac_toe = font2.render('Tic Tac Toe', True, WHITE)    # Renderiza el texto del título

# VARIABLES ******************************************************************

result = None                   # Resultado del juego (None, 'X Won', 'O Won', 'Draw')
line_pos = None                 # Posición de la línea ganadora
click_pos = None                # Posición del clic del mouse

running = True                  # Controla el bucle principal
while running:
    if result:
        win.blit(bg2, (0,5))    # Si hay resultado, muestra fondo 2
    else:
        win.blit(bg1, (0,5))    # Si no, muestra fondo 1

    pygame.draw.rect(win, BLUE, (10, 10, WIDTH-20, 50), border_radius=20)      # Dibuja rectángulo azul para el título
    pygame.draw.rect(win, WHITE, (10, 10, WIDTH-20, 50), 2, border_radius=20)  # Borde blanco al rectángulo
    win.blit(tic_tac_toe, (WIDTH//2-tic_tac_toe.get_width()//2,17))            # Dibuja el texto del título centrado
    
    for event in pygame.event.get():           # Procesa eventos
        if event.type == pygame.QUIT:          # Si se cierra la ventana
            running = False

        if event.type == pygame.KEYDOWN:       # Si se presiona una tecla
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # Si es ESC o Q
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:   # Si se presiona el mouse
            click_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:     # Si se suelta el mouse
            click_pos = None

    for box in box_list:                     # Para cada casilla
        box.update(win)                      # Actualiza su estado y la dibuja
        if box.active and click_pos:         # Si está activa y hubo clic
            if box.rect.collidepoint(click_pos):   # Si el clic fue dentro de la casilla
                box.active = False                # Desactiva la casilla
                box.text = text                   # Asigna el texto del jugador actual
                if text == 'X':
                    box.bgcolor = BLUE            # Si es X, fondo azul
                else:
                    box.bgcolor = ORANGE          # Si es O, fondo naranja

                board[box.index+1] = text        # Actualiza el tablero
                current_player = (current_player + 1) % 2  # Cambia de jugador
                text = players[current_player]            # Actualiza el texto

    check_winner = check_win(board, "X")     # Verifica si X ganó
    if not result and check_winner[0]:
        result = 'X Won'                     # Si ganó, actualiza resultado
        line_pos = check_winner[1]           # Guarda la línea ganadora
        scoreX += 1                          # Suma punto a X
    check_winner = check_win(board, "O")     # Verifica si O ganó
    if not result and check_winner[0]:
        result = 'O Won'                     # Si ganó, actualiza resultado
        line_pos = check_winner[1]           # Guarda la línea ganadora
        scoreO += 1                          # Suma punto a O
    if isBoardFull(board) or result:         # Si el tablero está lleno o hay resultado
        for box in box_list:
            box.active = False               # Desactiva todas las casillas
        if not result:
            result = 'Draw'                  # Si no hay ganador, es empate
    if line_pos:                             # Si hay línea ganadora
        starting = box_list[int(line_pos[0]) - 1].rect.center   # Punto inicial
        ending = box_list[int(line_pos[-1]) - 1].rect.center   # Punto final

        pygame.draw.line(win, WHITE, starting, ending, 5)      # Dibuja la línea ganadora

    if result:                               # Si hay resultado
        if box_list[-1].rect.bottom <= 500:  # Si las casillas no han bajado mucho
            for box in box_list:
                box.rect.y += 1              # Baja las casillas (animación)

        result_image = font3.render(result, True, WHITE)       # Renderiza el texto del resultado
        win.blit(result_image, (50, 210))                      # Lo dibuja en pantalla
        win.blit(replay_image, replay_rect)                    # Dibuja el botón de reinicio
        if click_pos and replay_rect.collidepoint(click_pos):  # Si se hace clic en el botón de reinicio
            board = create_board()                             # Reinicia el tablero
            box_list = generate_boxes()                        # Reinicia las casillas
            players = ['X', 'O']                               # Reinicia los jugadores
            current_player = random.randint(0, 1)              # Selecciona jugador inicial
            text = players[current_player]                     # Actualiza el texto

            result = None                                      # Limpia el resultado
            line_pos = None                                    # Limpia la línea ganadora

    if text == 'X':                                           # Si es turno de X
        pygame.draw.rect(win, BLUE, (35, 150, 80, 30), border_radius=10)    # Resalta X
    elif text == 'O':                                         # Si es turno de O
        pygame.draw.rect(win, ORANGE, (165, 150, 80, 30), border_radius=10) # Resalta O

    imgX = font1.render(f'X    {scoreX}', True, WHITE)        # Renderiza marcador de X
    imgO = font1.render(f'O    {scoreO}', True, WHITE)        # Renderiza marcador de O
    win.blit(imgX, (60, 152))                                 # Dibuja marcador de X
    win.blit(imgO, (180, 152))                                # Dibuja marcador de O
    pygame.draw.rect(win, WHITE, (35, 150, 80, 30), 1, border_radius=10)   # Borde marcador X
    pygame.draw.rect(win, WHITE, (165, 150, 80, 30), 1, border_radius=10)  # Borde marcador O

    pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)  # Borde negro de la ventana
    clock.tick()                                              # Controla la velocidad del bucle
    pygame.display.update()                                   # Actualiza la pantalla
pygame.quit()                                                # Sale de pygame